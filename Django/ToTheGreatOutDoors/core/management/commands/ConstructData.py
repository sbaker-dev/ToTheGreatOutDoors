from __future__ import annotations

from miscSupports import load_yaml, validate_path, load_json, write_json
from shapeObject.write_shapefile import set_polygon_geometry
from typing import Union, Optional, Dict, List, Tuple
from shapely.geometry import Polygon, MultiPolygon
from shapeObject import ShapeObject
from dataclasses import dataclass
from abc import abstractmethod
from pyproj import Transformer
from pathlib import Path


@dataclass()
class Location:
    """Data holder for locational data"""

    name: str
    gid: str
    purpose: str
    polygon: Union[Polygon, MultiPolygon]
    crs: str
    external_link: Optional[str] = None

    def overlap(self, overlap_places: List[Location]) -> Optional[Location]:
        """
        Validate if this locations polygon overlaps any place in the external_places. Return the external overlap
        Location if there is an overlap, None otherwise.
        """
        for location in overlap_places:
            if location.polygon.intersection(self.polygon).area > 0:
                return location
        return None

    def database_values(self, window_dimension: int, simplification: float, map_crs: str):
        """Convert to a dict for the json database"""
        return self.purpose, self.external_link, self.as_svg(window_dimension, simplification), self.centroid(map_crs)

    def as_svg(self, window_dimension: int, simplification: float):
        """Convert the svg points to be relative to the window dimension of the application"""
        polygon_points = self.polygon.simplify(tolerance=simplification)
        geometry_points = [[f"{x / window_dimension},{(y / window_dimension)} " for x, y in sub_geometry]
                           for i, sub_geometry in enumerate(set_polygon_geometry(polygon_points))]
        return "".join([f"M{p[0]}" + f"L{p[1]}" + f"{''.join(p[2:])}z" for p in geometry_points])

    def centroid(self, external_crs: str):
        """
        External maps CRS may not match the input, for example google maps CRS is EPSG:4326. This coverts the centroid
        of the polygon to a requested CRS so that it can be used for directions or other information.
        """
        transformer = Transformer.from_crs(self.crs, external_crs)
        centroid = self.polygon.centroid
        return transformer.transform(centroid.x, centroid.y)

    @property
    def place_name(self):
        """Many OS locations don't have a name, use the GID in this instance"""
        if len(self.name) <= 1:
            return self.gid
        else:
            return self.name


class DatabaseLoader:
    """Root class that all external shapefile will load via its abstract load_data"""

    def __init__(self, env: dict, shapefile_path: Union[str, Path]):
        self.shp = ShapeObject(validate_path(shapefile_path), encoding_errors='replace')
        self.env = env

    @abstractmethod
    def load_data(self, category: Optional[str] = None) -> Dict[str, Location]:
        """Construct a dictionary of type {name: Location} from the data within the shapefile"""


class NationalTrust(DatabaseLoader):
    """Read in data from a National Trust shapefile, and attempt to link in externally constructed links"""

    def __init__(self, env, shapefile_path):
        super().__init__(env, shapefile_path)

        self._link_data = load_json(Path(self.env['output_data_root'], 'NationalTrustLinks.txt'))

    def load_data(self, category: Optional[str] = None) -> Dict[str, Location]:
        # Extract the data from the shapefile
        locations_dict = {name: Location(name, gid, category, poly, 'epsg:27700')
                          for poly, (_, gid, name, _, _, _) in zip(self.shp.polygons, self.shp.records)}

        # Attempt to assign any links that are required if we find a match
        return {name: self.set_link(name, location) for name, location in locations_dict.items()}

    def set_link(self, location_name: str, location: Location) -> Location:
        """Search for a link that contains this locations name. If we find a link, assign it"""
        links_list = [link for name, link in self._link_data.items() if location_name.lower() in name.lower()]
        if len(links_list) > 0:
            location.external_link = links_list[0]
        return location


class EnglishHeritage(DatabaseLoader):
    """Read in data in from a English Heritage formatted shapefiles"""

    def __init__(self, env, shapefile_path, gid_i=0, name_i=1, link_i=-1):
        super().__init__(env, shapefile_path)

        # The number of columns is not consistent in the english heritage files. In theory the keyword defaults should
        # always work, but exposed for clarity and update potential
        self.gid_i = gid_i
        self.name_i = name_i
        self.link_i = link_i

    def load_data(self, category: Optional[str] = None) -> Dict[str, Location]:
        return {rec[self.name_i]: Location(rec[self.name_i], rec[self.gid_i], category, poly, 'epsg:27700',
                                           rec[self.link_i])
                for poly, rec in zip(self.shp.polygons, self.shp.records) if "cemetery" not in rec[self.name_i].lower()}


class OSGreenSpace(DatabaseLoader):
    """Loader for the OS green space data"""

    def __init__(self, env, shapefile_path, os_exceptions: List):
        super().__init__(env, shapefile_path)

        self.exceptions = os_exceptions

    def load_data(self, category: Optional[str] = None) -> Dict[str, Location]:
        return {gid: Location(name, gid, purpose, poly, 'epsg:27700') for poly, (gid, purpose, name, _, _, _) in
                zip(self.shp.polygons, self.shp.records) if purpose not in self.exceptions}


class OSBoundary(DatabaseLoader):
    """Loader for boundary data"""

    def __init__(self, env, shapefile_path):
        super().__init__(env, shapefile_path)

    def load_data(self, category: Optional[str] = None):
        return {name: Location(name, gid, category, poly, 'epsg:27700')
                for poly, (name, _, _, _, _, _, _, gid, _, _, _, _, _, _, _) in zip(
                self.shp.polygons, self.shp.records)}


class ConstructData:
    def __init__(self, env_path: Path, os_exceptions: List[str]):

        # Initialise the paths from the env file
        self.env = load_yaml(validate_path(env_path))
        self.os_data = self.env['os_data']
        self.data = self.env['external_data']

        # Canvas size for the SVG elements
        self.factory = {'national': NationalTrust, "english": EnglishHeritage}

        # Load the OS data and construct the database
        self.db, self.boundary, self.location_data = self._init_load_data(os_exceptions)

    def _init_load_data(self, os_exceptions: List[str]):
        """Load OS and other external databases"""

        # Load OS related data
        db, boundary, os_green = self._init_os_load(os_exceptions)

        # Load the rest of the external data, converge with os_green
        print("Loading external data...")
        location_data = [self._init_load_factory(datasource) for datasource in self.data] + [os_green]
        return db, boundary, location_data

    def _init_os_load(self, os_exceptions: List[str]) -> Tuple[dict, Dict[str, Location], Dict[str, Location]]:
        """
        Load the boundary data which we will use to relational map polygons to a region, and load the os green space
        data to check against external data. We only keep external places that do not exist in this master os green
        space dataset.
        """
        print("Loading Boundary Data...")
        boundary_path = self.os_data['os_boundary'] + "/GB/district_borough_unitary_region.shp"
        boundary = OSBoundary(self.env, boundary_path).load_data("Boundary")

        # Construct the database from the boundary data
        database = {place_name: [] for place_name, location in boundary.items()}

        print("Loading OS Green Space data...")
        os_data = OSGreenSpace(self.env, self.os_data['os_green'] + "/GB_GreenspaceSite.shp", os_exceptions).load_data()
        return database, boundary, os_data

    def _init_load_factory(self, datasource):
        """Instantiation of a given loader based on the first element of the data source key, split on underscore"""
        factory_class = self.factory[datasource.split("_")[0]]
        return factory_class(self.env, self.data[datasource]['link']).load_data(self.data[datasource]['category'])

    def relation_map(self):
        """
        Map each location within our datasets to a JSON database

        # Warning
        Not particularly optimised, will take a while.
        """
        # Note: This could be probably be spend up by using grid references...
        print("Assigning data to boundaries")
        [self._assign_location(i, place) for data in self.location_data for i, (name, place) in enumerate(data.items())]
        write_json(self.db, self.env['output_data_root'], 'RelationMap')

    def _assign_location(self, index: int, location: Location):
        """Assign a locations name to the database, if we find a location is within a boundary location"""
        if index % 1000 == 0:
            print(index)

        # Check that the location is within a given boundary zone, then assign if it is to the dict database
        boundary_name = location.overlap(list(self.boundary.values()))
        if not boundary_name:
            return
        self.db[boundary_name.name].append(location.place_name)
