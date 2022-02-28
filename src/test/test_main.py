"""test main"""
import pytest
from main import StreetAnalyser
from .config import TEST_IMAGE_PATHS


@pytest.mark.parametrize('path', TEST_IMAGE_PATHS)
def test_pipeline(path):
    """
    test pipeline
    Returns:

    """
    street_analyser = StreetAnalyser(test_mode=True)
    street_analyser.gui.path = path
    street_analyser.run()
    # street_analyser.gui.path = path
    # street_analyser.gui.b_start_callback()

    # street_analyser.interface_object.command_object.command_info['path'] = path
    # street_analyser.pipeline()
    assert_interface_object(street_analyser.interface_object)


def assert_interface_object(interface_object):
    """
    check if instance are not None
    Args:
        interface_object:

    Returns:

    """
    class_instances = [instance for instance in
                       dir(interface_object) if
                       not instance.startswith('__')]

    class_instances_visualization = [instance for instance in
                                     dir(interface_object.visualization_object) if
                                     not instance.startswith('__')]

    for class_instance_name in class_instances:
        class_instance = getattr(interface_object, class_instance_name)
        assert class_instance is not None

    for class_instance_name in class_instances_visualization:
        class_instance = getattr(interface_object.visualization_object, class_instance_name)
        assert class_instance is not None
