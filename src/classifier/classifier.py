"""Custom Classifier Module"""
import os
import pandas as pd
import cv2
import tensorflow.compat.v1 as tf  # pylint: disable=import-error
from .pipeline import NeuralNetwork, Session, build_pipeline


tf.disable_eager_execution()


class Classifier():
    """classify sign images into one of 42 classes / give probability for every class
    """

    def __init__(self, interface_object):
        """Initialize the classifier

        Args:
            interface_object (InterfaceObject): the interface_object containing the patches to
            be classified
        """
        self.pipeline = None
        self.sign_names = None
        self.initialize_session()
        self.interface_object = interface_object

    def initialize_session(self, ckpt_path=os.path.join('data',
                                                        'checkpoint',
                                                        'network10.ckpt')):
        """Initialize the checkpoint file:
        This function should be called in order to load a checkpoint file,
        and build a pipeline which can further generate the probabilities of different classes.

        This function should be called just ONCE (when the whole program starts)
        returns the pipeline and the list of sign names.
        """

        # Load sign_names
        sign_name_df = pd.read_csv(os.path.join('data', "sign_names.csv"),
                                   index_col='ClassId')
        self.sign_names = sign_name_df.SignName.values
        self.n_classes = len(self.sign_names)

        # Load session
        self.input_shape = (32, 32, 3)

        preprocessors = [resize_image, convert_to_rgb, normalizer]

        session = Session()
        self.pipeline = build_pipeline(preprocessors,
                                       session,
                                       self.make_network10())
        session.load(ckpt_path)

    def predict_proba(self):
        """ This function generates the array of probabilities,
            based on the interface_object and saves them in the
            interface_object.patches_list[i].probabilities.
        """
        # unpack the list
        images = [patch.patch for patch in self.interface_object.patches_list]

        # generate the probabilities
        prob_list = self.pipeline.predict_proba(images)

        # pack the list
        for patch, prob in zip(self.interface_object.patches_list, prob_list):
            patch.probabilities = prob
            patch.top_probabilities = sorted(zip(patch.probabilities, self.sign_names),
                                             key=lambda tup: -tup[0])

            # Take the first 5 probabilities
            patch.top_probabilities = patch.top_probabilities[:5]

    def make_network10(self):
        """Make the neural network

        Returns:
            NeuralNetwork: the Tensorflow NeuralNetwork
        """
        return (NeuralNetwork()
                .input(self.input_shape)
                .conv([5, 5, 24])
                .max_pool()
                .relu()
                .conv([5, 5, 64])
                .max_pool()
                .relu()
                .dropout(keep_prob=0.5)
                .flatten()
                .dense(480)
                .relu()
                .dense(self.n_classes))


def convert_to_rgb(image):
    """Convert to BGR to RGB.

    Args:
        image (ndarray): BGR opencv image

    Returns:
        ndarray: RBG opencv image
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def resize_image(image, shape=(32, 32)):
    """Resize the image

    Args:
        image (ndarray): the image
        shape (tuple, optional): input shape of the neural network. Defaults to (32, 32).

    Returns:
        ndarray: resized image
    """
    return cv2.resize(image, shape)


def normalizer(col_x):
    """Normalize a vector

    Args:
        col_x (ndarray): the vector

    Returns:
        ndarray: the normalized vector
    """
    return (col_x - col_x.mean()) / col_x.std()
