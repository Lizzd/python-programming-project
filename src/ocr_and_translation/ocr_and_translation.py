"""ocr and translation"""

from .sign_translator import SignTranslator
from .ocr import OCR


class OCRAndTranslation:
    """handeln the ocr and translation task"""

    def __init__(self, interface_object):
        """
        initialization
        Args:
            interface_object:
        """
        self.interface_object = interface_object
        self.ocr = OCR(self.interface_object)
        self.sign_translator = SignTranslator(self.interface_object)

    def apply_ocr_and_translation(self):
        """

        Returns:

        """
        if self.interface_object.command_object.ocr_and_trans['apply_ocr']:
            self.ocr.extract_strings()
            self.sign_translator.apply_translation()
            self.grab_command()

    def grab_command(self):
        """
        take the command object
        Returns:

        """
        command = self.interface_object.command_object.ocr_and_trans
        if not command['show_src_string']:
            for patch in self.interface_object.patches_list:
                patch.translation_info['src_string'] = "--"
        if not command['show_trans']:
            for patch in self.interface_object.patches_list:
                patch.translation_info['translation'] = "--"
