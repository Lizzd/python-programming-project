"""Test the classifier"""
import glob
import os
import time

import cv2
from classifier import Classifier
from objects import InterfaceObject
from .config import TEST_IMAGE_PATHS, DIRECTORIES_PATH


def test_prediction():
    """ Test if patch.probabilities has the correct size
    """

    path_list = TEST_IMAGE_PATHS
    interface_object = InterfaceObject()
    for count, path in enumerate(path_list):
        interface_object.add_patch(cv2.imread(path), [0, 0], [0, 0], count)
    clsf = Classifier(interface_object)
    clsf.predict_proba()
    for patch in interface_object.patches_list:
        # print(patch.probabilities, clsf.sign_names[np.argmax(patch.probabilities, axis=0)])
        # cv2.imshow("sign", patch.patch)
        # cv2.waitKey(1000)
        assert patch.probabilities.shape == (43,)


def test_speed():
    """Test if patch.probabilities has the correct size
    """

    path_list = glob.glob(os.path.join(DIRECTORIES_PATH['data'], "tsrd", "*")) + glob.glob(
        os.path.join(DIRECTORIES_PATH['data'], "tsrd-test", "*"))
    interface_object = InterfaceObject()
    for count, path in enumerate(path_list):
        interface_object.add_patch(cv2.imread(path), [0, 0], [0, 0], count)
    clsf = Classifier(interface_object)
    # print("Begin timing...")
    start_time = time.time()
    clsf.predict_proba()
    # print("End timing...")
    stop_time = time.time() - start_time
    print(f"For {len(interface_object.patches_list)} patches there were needed {stop_time} seconds")


def test_prediction_correctness():
    """Test if the prediction is correct, more or less.
    """

    path_list = [os.path.join('data', "sign_right.jpg")]
    interface_object = InterfaceObject()
    for count, path in enumerate(path_list):
        interface_object.add_patch(cv2.resize(cv2.imread(path), (400, 400)), [0, 0], [0, 0], count)
    clsf = Classifier(interface_object)
    clsf.predict_proba()
    for patch in interface_object.patches_list:
        # print(patch.top_probabilities[0])
        assert patch.top_probabilities[0][1] == "Turn right ahead"
