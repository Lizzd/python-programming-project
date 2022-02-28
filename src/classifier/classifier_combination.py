""" combine both classifiers classes into 1 class to reduce complexity when picking one classifier
"""
from .classifier import Classifier
from .classifier2 import Classifier2


class ClassifierCombination():
    """ read command option and start the spezified classifier
    (there are 2 different classifiers to choose from)
    """

    def __init__(self, interface_object):
        self.command_object = interface_object.command_object
        self.class1 = Classifier(interface_object)
        self.class2 = Classifier2(interface_object)

    def predict_proba(self):
        """apply the classifier specified in self.command_object
            on given patches of a frame (=interface_object)
        """
        classifier_model = self.command_object.classifier["classifier_model"]
        if classifier_model == 0:
            self.class1.predict_proba()
        else:
            self.class2.predict_proba()

    def predict_proba_double(self):
        """predict_proba for both Classifer 1 & 2
        """
