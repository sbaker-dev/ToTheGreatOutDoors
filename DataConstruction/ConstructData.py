from __future__ import annotations

import sys

from miscSupports import load_yaml, validate_path, load_json, terminal_time
from dataclasses import dataclass
from shapely.geometry import Polygon, MultiPolygon
from typing import Union, Optional, Dict, List
from pathlib import Path
from shapeObject import ShapeObject
from shapeObject.write_shapefile import set_polygon_geometry
from abc import abstractmethod


@dataclass()
class Location:
    """Data holder for locational data"""

    name: str
    gid: str
    purpose: str
    polygon: Union[Polygon, MultiPolygon]
    external_link: Optional[str] = None

    def overlap(self, os_places: List[Location]):
        for location in os_places:
            if location.polygon.intersection(self.polygon).area > 0:
                return True
        return False

    def as_svg(self, window_dimension: int):
        geometry_points = [[f"{x / window_dimension},{(y / window_dimension)} " for x, y in sub_geometry]
                           for i, sub_geometry in enumerate(set_polygon_geometry(self.polygon))]

        return "".join([f"M{p[0]}" + f"L{p[1]}" + f"{''.join(p[2:])}z" for p in geometry_points])


class DatabaseLoader:
    """Root class that all external shapefile will load via its abstract load_data"""

    def __init__(self, shapefile_path):
        self.shp = ShapeObject(validate_path(shapefile_path), encoding_errors='replace')

    @abstractmethod
    def load_data(self, category: Optional[str] = None) -> Dict[str, Location]:
        """Construct a dictionary of type {name: Location} from the data within the shapefile"""


class NationalTrust(DatabaseLoader):
    """Read in data from a National Trust shapefile, and attempt to link in externally constructed links"""

    def __init__(self, shapefile_path):
        super().__init__(shapefile_path)

        self._link_data = load_json(Path(Path(__file__).parent.parent, "Data", 'NationalTrustLinks.txt'))

    def load_data(self, category: Optional[str] = None) -> Dict[str, Location]:
        # Extract the data from the shapefile
        locations_dict = {name: Location(name, gid, category, poly)
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

    def __init__(self, shapefile_path, gid_i=0, name_i=1, link_i=-1):
        super().__init__(shapefile_path)

        # The number of columns is not consistent in the english heritage files. In theory the keyword defaults should
        # always work, but exposed for clarity and update potential
        self.gid_i = gid_i
        self.name_i = name_i
        self.link_i = link_i

    def load_data(self, category: Optional[str] = None) -> Dict[str, Location]:
        return {rec[self.name_i]: Location(rec[self.name_i], rec[self.gid_i], category, poly, rec[self.link_i])
                for poly, rec in zip(self.shp.polygons, self.shp.records) if "cemetery" not in rec[self.name_i].lower()}


class OSGreenSpace(DatabaseLoader):
    """Loader for the OS green space data"""

    def __init__(self, shapefile_path, os_exceptions: List):
        super().__init__(shapefile_path)

        self.exceptions = os_exceptions

    def load_data(self, category: Optional[str] = None) -> Dict[str, Location]:
        return {name: Location(name, gid, purpose, poly) for poly, (gid, purpose, name, _, _, _) in
                zip(self.shp.polygons, self.shp.records) if purpose not in self.exceptions}


class OSBoundary(DatabaseLoader):
    """Loader for boundary data"""

    def __init__(self, shapefile_path):
        super().__init__(shapefile_path)

    def load_data(self, category: Optional[str] = None) -> Dict[str, Location]:
        return {name: {"Geography": Location(name, gid, category, poly), 'Locations': []}
                for poly, (name, _, _, _, _, _, _, gid, _, _, _, _, _, _, _) in zip(
                self.shp.polygons, self.shp.records)}


class ConstructData:
    def __init__(self, window_size: int, os_exceptions: List[str]):
        env = load_yaml(validate_path(Path(Path(__file__).parent.parent, 'env.yaml')))
        self.os_data = env['os_data']
        self.data = env['external_data']

        self.database, self.os_green = self._init_os_load(os_exceptions)

        # Canvas size for the SVG elements
        self.window_size = window_size
        self.factory = {'national': NationalTrust, "english": EnglishHeritage}

    def _init_os_load(self, os_exceptions: List[str]):
        """
        Load the boundary data which we will use to relational map polygons to a region, and load the os green space
        data to check against external data. We only keep external places that do not exist in this master os green
        space dataset.
        """
        print("Loading Boundary Data...")
        boundary_path = self.os_data['os_boundary'] + "/GB/district_borough_unitary_region.shp"
        boundary = OSBoundary(boundary_path).load_data("Boundary")

        print("Loading OS Green Space data...")
        os_data = OSGreenSpace(self.os_data['os_green'] + "/GB_GreenspaceSite.shp", os_exceptions).load_data()

        return boundary, os_data

    def main(self):

        print("Loading external data...")
        other_external_data = [self.load_factory(datasource) for datasource in self.data]

        # TODO: We need to link the locations to a county
        # TODO: Basically we need to change overlap to return the overlap, so that way we want a null return for the
        #   os check overlap, but when we have a county, we want the actual value.

        # Note: This could be spend up by isolating OS green space areas within the same grid reference as the current
        # external location. Would need to have a point coordinate to grid map reference category for that to work.
        for data in other_external_data:
            for name, location in data.items():
                if not location.overlap(list(self.os_green.values())):
                    print(location.as_svg(self.window_size))
                    print("TRUE")
                    print(name)
                    sys.exit()

        # NationalTrust(self.env['national_trust_open']).load_data("National Trust")
        # NationalTrust(env['national_trust_limited']).load_data("National Trust")
        # EnglishHeritage(env['english_heritage_parks']).load_data("Public Park Or Garden")
        # EnglishHeritage(env['english_heritage_monuments']).load_data("Monuments")

    def load_factory(self, datasource):
        """Instantiation of a given loader based on the first element of the data source key, split on underscore"""
        elements = datasource.split("_")
        return self.factory[elements[0]](self.data[datasource]['link']).load_data(self.data[datasource]['category'])


if __name__ == '__main__':
    exceptions = ['Religious Grounds', 'Allotments Or Community Growing Spaces', 'Cemetery']
    ConstructData(2000, exceptions).main()
