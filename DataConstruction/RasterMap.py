from miscSupports import load_yaml, directory_iterator, write_json
from imageObjects import ImageObject
from imageObjects.Support import load_image
from pathlib import Path
import exifread


class ReformatRaster:
    def __init__(self, env_path: Path, window_size: int):

        self.env = load_yaml(env_path)
        self.root = load_yaml(env_path)['os_data']['os_raster']
        self.window_size = window_size
        self.raster_positions = {}

    def __call__(self, *args, **kwargs):
        """Create a PNG of each tiff, and save the position data to a database"""
        [self.reformat_tiffs(file) for file in directory_iterator(self.root)]

        write_json(self.raster_positions, self.env['output_data_root'], 'RasterPositions')

    def reformat_tiffs(self, file_name: str):
        """Convert the tiff into a png and store the coordinate data for django"""
        print(file_name)
        # Covert the flipped image (vertically) into a png, and save to the Django static directory
        self.convert_to_png(file_name)

        # Extract the images
        self.extract_meta_data(file_name)

    def convert_to_png(self, file_name: str):
        """
        As all our point data is inverse, we need to rotate the svg canvas by 180. Therefore, the images need to
        inverted vertically. SVGs also require png / jpg, so we need to store them as pngs, not tiffs.
        """
        img = ImageObject(load_image(Path(self.root, file_name)))
        img.flip_vertical()
        img.write_to_file(Path(Path(__file__).parent.parent, 'Django', 'static', 'images'), Path(file_name).stem)

    def extract_meta_data(self, file_name: str):
        """Isolate the meta data, specifically the starting map location, as we need that to place the map"""
        tiff_file = open(Path(self.root, file_name), 'rb')

        # Extract the start location from 0x8482
        tags = exifread.process_file(tiff_file)
        _, _, _, start_x, start_y, _ = tags['Image Tag 0x8482'].values

        # Assign the x and y relative to the window size, then close the file
        self.raster_positions[Path(file_name).stem] = {"X": start_x[0] / self.window_size,
                                                       "Y": start_y[0] / self.window_size}
        tiff_file.close()


if __name__ == '__main__':
    ReformatRaster(Path(Path(__file__).parent.parent, "env.yaml"), 2000)()
