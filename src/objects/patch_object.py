"""this object get passed around between the different process"""


class PatchObject:
    """contains all information about a Patch = a small image that is part
    of the whole frame. There Patches are detected in Preprocessing as (possibly)
    showing a sign. Next they are classified next and later they are shown on the right
    side of the GUI."""

    def __init__(self, patch, patch_id=0):
        """initalize the attribute"""

        self.patch = patch

        self.probabilities = None
        self.top_probabilities = None  # list of tuples (probability, label)

        self.class_strings = None
        self.class_id = None
        self.translation_info = {'patch_id': patch_id, 'src_string': None,
                                 'detected_language': None, 'translation': None}

        # position: [pos_x,pos_y] represent the top left corner of the patch in the original frame
        self.position = [0, 0]
        # size: [width, height]
        self.size = [0, 0]

    def update_position(self, posistion):
        """update the position"""
        self.position = posistion

    def update_size(self, size):
        """update the size"""
        self.size = size

    def scale_patch(self):
        """#TODO"""
        return self
