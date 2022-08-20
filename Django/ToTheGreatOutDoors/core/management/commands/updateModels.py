from django.core.management.base import BaseCommand
from ...models import TravelLocation, Boundary, RasterMap

from .ConstructData import ConstructData, Location

from miscSupports import load_json, load_yaml
from pathlib import Path


class Command(BaseCommand):
    def __init__(self):
        super().__init__()

        # Environment
        self.env_root = Path(Path(__file__).parent.parent.parent.parent.parent.parent, 'env.yaml')
        self.env = load_yaml(self.env_root)

        # Assignable args
        self.window_size = None
        self.boundary_simplify = None
        self.place_simplify = None
        self.place_relations = None

    help = 'import booms'

    def add_arguments(self, parser):
        parser.add_argument('window_size', nargs='+', type=int, help='The size of the svg canvas')
        parser.add_argument('boundary_simplification', nargs='+', type=float,
                            help='The simplification boundary polygon geometry, assign 1.0 for no simplification')
        parser.add_argument('place_simplification', nargs='+', type=float,
                            help='The simplification location polygon geometry, assign 1.0 for no simplification')

    def handle(self, *args, **kwargs):
        # Initialise the required key word args
        self._initialise_arguments(kwargs)

        # Construct the json databases from the location data
        location_database = self._location_database()

        # Construct the boundary polygonal table
        self._construct_boundaries(location_database)

        # Construct the raster image table
        self._construct_raster()

        # Construct the location table
        self._construct_locations(location_database)

    def _initialise_arguments(self, kwargs: dict):
        """Initialise the arguments from the command line to __init__"""
        self.window_size = kwargs['window_size'][0]
        self.boundary_simplify = kwargs['boundary_simplification'][0]
        self.place_simplify = kwargs['place_simplification'][0]

        # Load the relational data for locations
        relations_db = load_json(self.env['output_data_root'] + "/RelationMap.txt")
        self.place_relations = {location: place for place, relation in relations_db.items() for location in relation}

    def _location_database(self):
        """Construct the {name: Location} database by loading each of the shapefiles entries as Location"""
        # TODO: Expose?
        exclusions = ['Religious Grounds', 'Allotments Or Community Growing Spaces', 'Cemetery']
        return ConstructData(self.env_root, exclusions)

    def _construct_boundaries(self, location_database: ConstructData):
        """Construct the Boundaries within the db.sqlite3 database"""
        print("Assigning boundary locations...")
        boundary_list = [Boundary(place=place, svg=data.as_svg(self.window_size, self.boundary_simplify))
                         for place, data in location_database.boundary.items()]
        Boundary.objects.bulk_create(boundary_list)

    def _construct_locations(self, location_db: ConstructData):
        """Assign each travel location to the database"""
        print("Assigning travel location...")
        location_database = [self._assign_locations(name, place, database_index, place_index)
                             for database_index, database in enumerate(location_db.location_data)
                             for place_index, (name, place) in enumerate(database.items())]
        location_database = [location for location in location_database if location]
        TravelLocation.objects.bulk_create(location_database)

    def _assign_locations(self, name: str, place: Location, database_index: int, place_index: int):
        """Assign a location, if it can be placed within a relational map"""
        if place_index % 100 == 0:
            print(f"Assigned {place_index} locations from database {database_index}")
        try:
            purpose, external_link, svg_data, (x, y), = \
                place.database_values(self.window_size, self.place_simplify, 'epsg:4326')
            return TravelLocation(name=name, category=purpose, svg=svg_data, link=external_link,
                                  place=self.place_relations[name], map_x=x, map_y=y)
        except KeyError:
            pass

    def _construct_raster(self):
        """Assign the raster location data"""
        print("Assigning raster data")
        raster_data = load_json(self.env['output_data_root'] + "/RasterPositions.txt")
        raster_database = [RasterMap(place=map_name, x=map_values['X'], y=map_values['Y'], size=map_values['Size'])
                           for map_name, map_values in raster_data.items()]
        RasterMap.objects.bulk_create(raster_database)
