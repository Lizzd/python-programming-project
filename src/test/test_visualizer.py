"""test"""

from visualization import Visualizer
from objects import InterfaceObject
from .config import TEST_IMAGE_1, TEST_IMAGE_3


def test_frame_annotation():
    """

    Returns:

    """
    interface_object = InterfaceObject()
    pre_frame = interface_object.visualization_object.final_annotated_frame
    visualizer = Visualizer(interface_object)

    image = TEST_IMAGE_1
    interface_object.frame_dict['original'] = image
    visualizer.process()
    assert pre_frame is not interface_object.visualization_object.final_annotated_frame
    assert interface_object.visualization_object.final_annotated_frame is not None


def test_patch_and_frame():
    """

    Returns:

    """
    interface_object = InterfaceObject()
    visualizer = Visualizer(interface_object)

    image = TEST_IMAGE_1
    interface_object.frame_dict['original'] = image
    visualizer.process()
    assert interface_object.visualization_object.final_annotated_frame is not None


def test_combination_to_patch_and_icon_list():
    """

    Returns:

    """
    interface_object = InterfaceObject()
    visualizer = Visualizer(interface_object)
    visualizer.frame = TEST_IMAGE_3
    visualizer.patch_list = [TEST_IMAGE_3]
    visualizer.icon_list = [visualizer.frame]

    visualizer.combination_to_patch_and_icon_list()
    assert visualizer.patch_and_icon_list is not None
    assert isinstance(visualizer.patch_and_icon_list, list)


def test_compute_best_fg_color_for_the_translation_text():
    """

    Returns:

    """
    translation_pos = [425, 745]
    interface_object = InterfaceObject()
    visualizer = Visualizer(interface_object)
    visualizer.frame = TEST_IMAGE_3

    output = visualizer.compute_best_fg_color_for_the_translation_text(translation_pos[0],
                                                                       translation_pos[1])
    assert_datatype(output)


def test_compute_best_fg_color_for_the_strings_text():
    """

    Returns:

    """
    string_pos = [425, 730]
    interface_object = InterfaceObject()
    visualizer = Visualizer(interface_object)
    visualizer.frame = TEST_IMAGE_3

    output = visualizer.compute_best_fg_color_for_the_strings_text(string_pos[0], string_pos[1])
    assert_datatype(output)


def assert_datatype(output):
    """
    assert the data type and value range
    Args:
        output:

    Returns:

    """
    assert output is not None
    assert isinstance(output, tuple)
    for element in output:
        assert isinstance(element, int)
        assert 0 <= element <= 255
