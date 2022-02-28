"""These are the pytests to test the GUI"""
from gui import GUIVisual, GUIVideo
from objects import InterfaceObject


class TestGUIClass:
    """Unit tests for GUI """

    @staticmethod
    def test_gui():
        """Test the GUI"""
        interface_object = InterfaceObject()
        gui_visual = GUIVisual(interface_object)
        class_instances = [instance for instance in
                           dir(gui_visual) if
                           not instance.startswith('__') and not instance.startswith('_')]

        for class_instance_name in class_instances:
            class_instance = getattr(gui_visual, class_instance_name)
            assert class_instance is not None

    @staticmethod
    def test_gui_video():
        """Test the GUI"""
        interface_object = InterfaceObject()

        gui_visual = GUIVisual(interface_object)

        params = (gui_visual.master, gui_visual.canvas_vid,
                  gui_visual.canvas_desc, gui_visual.canvas_desc_2,
                  gui_visual.recorder)
        gui_video = GUIVideo(params, interface_object)
        class_instances = [instance for instance in
                           dir(gui_video) if
                           not instance.startswith('__') and not instance.startswith('_')]

        for class_instance_name in class_instances:
            class_instance = getattr(gui_video, class_instance_name)
            assert class_instance is not None
