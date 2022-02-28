"""test logic Class
"""
import os
import random
import imageio
import numpy as np
from logic import Logic
from objects import InterfaceObject
from .config import DIRECTORIES_PATH


def test_logic_basic():
    """test basic function of Class logic
    """

    def create_icon_path(sign_number):
        """give path to specific icon image

        Args:
            sign_number (int): sign  id

        Returns:
            path: path to specific icon image
        """
        dir_path = DIRECTORIES_PATH['icons']
        if sign_number < 10:
            zero = "0"
        else:
            zero = ""
        return dir_path + os.sep + zero + str(sign_number) + ".png"

    interface_object = InterfaceObject()
    log = Logic(interface_object)

    example_pic = np.zeros((32, 32, 3))
    random_int = random.randint(0, 42)
    random_propability_vector = np.zeros((43))
    random_propability_vector[random_int] = 1
    icon = imageio.imread(create_icon_path(random_int))[:, :, :3]

    interface_object.add_patch(example_pic, [0, 0], [0, 0])
    interface_object.patches_list[0].probabilities = random_propability_vector

    log.apply_logic()
    important_patch_list = interface_object.important_patches
    icon_list = interface_object.icon_list

    assert np.array_equal(important_patch_list[0], example_pic)
    assert np.array_equal(icon_list[0], icon)
