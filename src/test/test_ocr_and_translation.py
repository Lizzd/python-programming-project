""" Test the OCR function"""
import time

import cv2
import pytest

from ocr_and_translation import OCR, OCRAndTranslation
from objects import InterfaceObject
from .config import TEST_IMAGE_1, TEST_IMAGE_2


def test_strings():
    """Test the strings.
    """
    # Load Image and Initialize the OCR
    my_image = TEST_IMAGE_1

    my_image = cv2.cvtColor(my_image, cv2.COLOR_BGR2RGB)
    interface_object = InterfaceObject(my_image)
    interface_object.add_patch(my_image, [0, 0], [0, 0])
    ocr = OCR(interface_object)
    ocr.extract_strings()
    # print(interface_object.patches_list[0].translation_info['src_string'])
    assert interface_object.patches_list[0].translation_info['src_string'] == "SPEED LIMIT"


def test_speed():
    """Test the speed.
    """
    # Load Image and Initialize the OCR
    my_image = TEST_IMAGE_1

    my_image = cv2.cvtColor(my_image, cv2.COLOR_BGR2RGB)
    interfaceobject = InterfaceObject(my_image)
    interfaceobject.add_patch(my_image, [0, 0], [0, 0])
    ocr = OCR(interfaceobject)
    start_time = time.time()
    ocr.extract_strings()
    stop_time = time.time() - start_time
    # print(interfaceobject.patches_list[0].translation_info['src_string'])
    print(f" There were needed {stop_time} seconds")
    assert interfaceobject.patches_list[0].translation_info['src_string'] == "SPEED LIMIT"


def test_no_string():
    """Test for an image that does not contain any strings.
    """
    # Load Image and Initialize the OCR
    my_image = TEST_IMAGE_2

    my_image = cv2.cvtColor(my_image, cv2.COLOR_BGR2RGB)
    interfaceobject = InterfaceObject(my_image)
    interfaceobject.add_patch(my_image, [0, 0], [0, 0])
    ocr = OCR(interfaceobject)
    ocr.extract_strings()
    assert interfaceobject.patches_list[0].translation_info['src_string'] == ""


@pytest.mark.parametrize('info_key,command_key',
                         [('src_string', 'apply_ocr'), ('detected_language', 'show_src_string'),
                          ('translation', 'show_trans')])
def test_grab_command(info_key, command_key):
    """
    test
    Returns:

    """
    interface_object = InterfaceObject()
    if interface_object.command_object.ocr_and_trans[command_key] == 0:
        ocr_and_translation = OCRAndTranslation(interface_object)
        ocr_and_translation.grab_command()
        for patch in interface_object.patches_list:
            assert patch.translation_info[info_key] is None
