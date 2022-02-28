"""This module recognizes the string in an image_file"""
from PIL import Image, ImageOps
import tesserocr


class OCR:
    """optical character recognition: detect words on possible signs (patches)
    """

    def __init__(self, interface_object):
        """Initialize the OCR

        Args:
            interface_object (InterfaceObject): the interface object
        """
        self.interface_object = interface_object
        self.api = tesserocr.PyTessBaseAPI()

    def extract_strings(self):
        """Extract the strings from the image.
        """
        for patch in self.interface_object.patches_list:
            tess_image = Image.fromarray(patch.patch)

            # Get Strings and remove trailing and leading whitespaces
            self.api.SetImage(tess_image)
            string_list = [self.api.GetUTF8Text().strip()]
            self.api.SetImage(ImageOps.invert(tess_image))
            string_list.append(self.api.GetUTF8Text().strip())

            # Choose the longest as the string we have identified
            patch.translation_info['src_string'] = string_list[1] \
                if len(string_list[1]) > len(string_list[0]) \
                else string_list[0]

            # Replace all newlines with spaces
            patch.translation_info['src_string'] = patch.translation_info['src_string'].replace(
                '\n', " ")

    def placeholder(self):
        """

        Returns:

        """
        return self
