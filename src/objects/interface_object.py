"""Interface Object"""
import copy
from .patch_object import PatchObject
from .commands_object import CommandsObject
from .visualization_object import VisualizationObject


class InterfaceObject():
    """Interface Object: all information of the current frame is stored in
    an object of this class and used to transport this information bewtween
    preprocessor, classifier and logic.
    The object is updated for every frame of the video.
    """

    def __init__(self, frame=None):
        """ init """
        self.patches_list = []

        self.command_object = CommandsObject()
        self.visualization_object = VisualizationObject()

        annotate_frame = copy.deepcopy(frame)
        self.frame_dict = {'original': frame, 'default': annotate_frame}
        # patches to show on the side of the GUI
        self.important_patches = []
        # corresponding icons of the patches
        self.corresponding_icons = []
        self.icon_list = []

        self.is_image = False

    def add_patch(self, patch_array, position, size, patch_id=0):
        """
        Add Patch
        Args:
            patch_array:
            position:
            size:
            patch_id:

        Returns:

        """
        patch = PatchObject(patch_array, patch_id)
        patch.update_position(position)  # position[0] is x
        patch.update_size(size)  # size[0] is width
        self.patches_list.append(patch)

    def reset(self):
        """
        reset the interface object
        Returns:

        """
        self.important_patches = []
        self.icon_list = []
        self.patches_list = []

    def update_frame(self, frame):
        """

        Args:
            frame:

        Returns:

        """
        self.frame_dict['original'] = frame

    def add_frame_to_frame_dict(self, frame, frame_name):
        """

        Args:
            frame:
            frame_name:

        Returns:

        """
        self.frame_dict[frame_name] = frame

    def delete_frame_from_frame_dict(self, frame_name_to_pop):
        """

        Args:
            frame_name_to_pop:

        Returns:

        """
        self.frame_dict.pop(frame_name_to_pop)

    def get_list_from_frame_dict(self):
        """
        convert frame dict to a list
        Returns:

        """
        return list(self.frame_dict.items())

    def refresh_frame_dict(self):
        """
        delete the preprocessor specific element from dict
        Returns:

        """
        name_list = []
        for frame_name, _frame in self.frame_dict.items():
            if frame_name not in ["original", "default"]:
                name_list.append(frame_name)
        for frame_name in name_list:
            self.frame_dict.pop(frame_name)
