"""This is the main script"""
import threading

from utils import frame_generator
from objects import InterfaceObject
from preprocess import Preprocessor

from ocr_and_translation.ocr_and_translation import OCRAndTranslation

from gui import GUIVisual
from classifier import ClassifierCombination as Classifier
from visualization import Visualizer
from logic import Logic


# pylint: disable=too-many-instance-attributes


class StreetAnalyser():
    """main method"""

    def __init__(self, test_mode=False):

        self.interface_object = InterfaceObject()
        self.preprocessor = Preprocessor(self.interface_object)
        self.ocr_and_translation = OCRAndTranslation(self.interface_object)

        self.events = {"has_started": threading.Event(),
                       "run_pipeline": threading.Event(),
                       "run_gui": threading.Event(),
                       "pause": threading.Event(),
                       "stop": threading.Event()}

        self.gui = GUIVisual(self.interface_object, self.events, test_mode)

        self.clsf = Classifier(self.interface_object)
        self.visulizer = Visualizer(self.interface_object)
        self.logic = Logic(self.interface_object)

    def run(self):
        """main processing loop"""
        secondary_thread = threading.Thread(target=self.pipeline)
        secondary_thread.setDaemon(True)
        secondary_thread.start()

        self.gui.run()

    def pipeline(self):
        """
        pipeline: the main calculation loop
        Returns:

        """

        while True:

            self.events["has_started"].wait()
            media_path = self.interface_object.command_object.command_info['path']

            for frame in frame_generator(media_path, self.events):
                self.interface_object.reset()
                self.events["run_pipeline"].wait()
                self.interface_object.update_frame(frame)

                self.preprocessor.process()

                self.clsf.predict_proba()
                self.ocr_and_translation.apply_ocr_and_translation()
                self.logic.apply_logic()
                self.visulizer.process()

                self.events["run_pipeline"].clear()
                self.events["run_gui"].set()
            self.events["has_started"].clear()


if __name__ == '__main__':
    ANALYSER = StreetAnalyser()
    ANALYSER.run()
