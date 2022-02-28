"""this class handle the preprocessing tasks"""
import copy
from .shapedetection import ShapeDetector
from .mser import MSER
from .color_analyser import ColorAnalyser


class Preprocessor():
    """detect parts of the Frame that could contain a sign
    """

    def __init__(self, interface_object=None):
        """initialize the attribute"""
        self.list_of_frame_patches = []
        self.frame = None

        self.featute_extractor = None
        self.interface_object = interface_object

        self.command = None
        self.previous_command = None

    def process(self):
        """the main method of the preprocess"""
        self.grab_command()
        frame = self.interface_object.frame_dict['original']
        self.interface_object.frame_dict['default'] = copy.deepcopy(frame)
        self.featute_extractor.extract_shapes(frame)

    def grab_command(self):
        """
        take the command object
        Returns:

        """
        self.command = self.interface_object.command_object.preprocessor['features_extractor']
        if self.previous_command != self.command:
            self.interface_object.refresh_frame_dict()
        if self.command == 0:
            self.featute_extractor = ColorAnalyser(self.interface_object)
        elif self.command == 1:
            self.featute_extractor = ShapeDetector(self.interface_object)
        else:
            self.featute_extractor = MSER(self.interface_object)
        self.previous_command = self.command
