"""test preprocessor"""
import cv2
import pytest
from preprocess import Preprocessor, ColorAnalyser
from objects import InterfaceObject
from .config import TEST_IMAGE_PATHS


def assert_frame_characters(frame1, frame2):
    """
    assert characters from two image
    Args:
        frame1:
        frame2:

    Returns:

    """
    assert frame1 is not None
    assert frame2 is not None
    assert frame1 is not frame2
    assert frame1.shape == frame2.shape


@pytest.mark.parametrize('path', TEST_IMAGE_PATHS)
def test_shape(path):
    """
    test
    Returns:

    """
    interface_object = InterfaceObject()
    interface_object.command_object.preprocessor['features_extractor'] = 0
    preprocessor = Preprocessor(interface_object)

    image = cv2.imread(path)
    interface_object.frame_dict['original'] = image
    preprocessor.process()
    output_image = interface_object.frame_dict['default']
    assert_frame_characters(image, output_image)


@pytest.mark.parametrize('path', TEST_IMAGE_PATHS)
def test_mser(path):
    """
    test
    Returns:

    """
    interface_object = InterfaceObject()
    interface_object.command_object.preprocessor['features_extractor'] = 1

    preprocessor = Preprocessor(interface_object)

    image = cv2.imread(path)
    interface_object.frame_dict['original'] = image
    preprocessor.process()
    output_image = interface_object.frame_dict['default']
    assert_frame_characters(image, output_image)


@pytest.mark.parametrize('path', TEST_IMAGE_PATHS)
def test_update_patch_object(path):
    """
    test update patch object
    Returns:

    """
    interface_object = InterfaceObject()
    color_analyser = ColorAnalyser(interface_object)
    previous_contours = color_analyser.contours

    frame = cv2.imread(path)
    interface_object.frame_dict['original'] = frame

    color_analyser.extract_shapes(frame)
    assert previous_contours is not color_analyser.contours
    assert color_analyser.contours is not None


@pytest.mark.parametrize('path', TEST_IMAGE_PATHS)
def test_hsv_color_filter(path):
    """
    test filter
    Returns:

    """
    interface_object = InterfaceObject()
    color_analyser = ColorAnalyser(interface_object)
    frame = cv2.imread(path)
    interface_object.frame_dict['original'] = frame
    color_analyser.extract_shapes(frame)
    mask = color_analyser.apply_hsv_color_filter(frame)
    assert_frame_characters(mask, frame[..., 0])


@pytest.mark.parametrize('extractor_id,extractor_name',
                         [(0, 'ColorAnalyser'), (1, 'ShapeDetector'), (2, 'MSER')])
def test_grab_command(extractor_id, extractor_name):
    """
    test
    Returns:

    """
    interface_object = InterfaceObject()
    interface_object.command_object.preprocessor['features_extractor'] = extractor_id

    preprocessor = Preprocessor(interface_object)
    preprocessor.grab_command()
    assert type(preprocessor.featute_extractor).__name__ == extractor_name
