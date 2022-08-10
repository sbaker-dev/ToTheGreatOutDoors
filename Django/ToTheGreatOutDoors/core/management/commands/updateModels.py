from django.core.management.base import BaseCommand
from ...models import Place, Location, Boundary

from .ConstructData import ConstructData

from miscSupports import load_json, load_yaml, terminal_time
from pathlib import Path


class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        return

    def handle(self, *args, **kwargs):

        # Arguments, should probably allow to set externally
        window_size = 2000
        boundary_simplification = 10.0
        place_simplification = 1.0

        env_root = Path(Path(__file__).parent.parent.parent.parent.parent.parent, 'env.yaml')
        env = load_yaml(env_root)

        # Setup the place-relation and relation-place databases
        relations_database = load_json(env['output_data_root'] + "/RelationMap.txt")
        place_relations = {location: place for place, relation in relations_database.items() for location in relation}

        # Construct the location data
        exclusions = ['Religious Grounds', 'Allotments Or Community Growing Spaces', 'Cemetery']
        location_database = ConstructData(env_root, window_size, exclusions)

        print("Assigning boundary locations...")
        for place, data in location_database.boundary.items():
            place = Place(name=place)
            place.save()

            boundary = Boundary(place=place, svg=data.as_svg(window_size, boundary_simplification))
            boundary.save()

        print("Assigning place names...")
        for place in relations_database.keys():
            models = Place(name=place)
            models.save()

        print("Assigning Location data...")
        for i, database in enumerate(location_database.location_data):
            print(f"For database {i} Locations: {terminal_time()}")
            for name, place in database.items():

                try:
                    relation_place = Place(name=place_relations[name])
                    relation_place.save()

                    purpose, external_link, svg_data = place.database_values(window_size, place_simplification)
                    location = Location(name=name, category=purpose, svg=svg_data, link=external_link,
                                        place=relation_place)
                    location.save()
                except KeyError:
                    pass
