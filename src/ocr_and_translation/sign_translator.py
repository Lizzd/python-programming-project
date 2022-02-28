"""Translation class"""
from googletrans import Translator


class SignTranslator:
    """Translate text on signs"""

    def __init__(self, interface_object=None):
        """
        initialization
        Args:
            interface_object:
        """
        self.confidence = None
        self.translator = Translator()
        self.interface_object = interface_object
        self.source_language = None

    def apply_translation(self):
        """
        method that gets called by main
        Returns:

        """
        for patch in self.interface_object.patches_list:
            if patch.translation_info['src_string'] is not None:
                src_string = patch.translation_info['src_string']
                self.language_detection(src_string)
                patch.translation_info['detected_language'] = self.source_language
                translated_string = self.add_translation_text(src_string)
                patch.translation_info['translation'] = translated_string

    def add_translation_text(self, text, dest_language='en'):
        """
        translate the text into the destination language
        Args:
            text:
            dest_language:

        Returns:

        """
        try:
            text = self.translator.translate(text, dest=dest_language).text
        except ValueError:
            text = self.translator.translate(text).text
        return text

    def language_detection(self, text):
        """
        detect the language
        Args:
            text:

        Returns:

        """
        detector = self.translator.detect(text)
        self.source_language = detector.lang
        self.confidence = detector.confidence
