"""use color information to detecte candidates for the classifier"""
import copy
import threading
import glob
import cv2
import numpy as np
from preprocess.preprocess_utils import morphology_operation
from preprocess.preprocess_utils import filter_contours_by_aspect_ratio, filter_contours_by_area
from preprocess.preprocess_utils import filter_contours_by_edge_number
from objects.interface_object import InterfaceObject
from utils.utils import frame_generator


class ColorAnalyser:
    """detect signs on a frame based on their colors"""

    def __init__(self, interface_object=None):
        """initial the attributes of the gui object"""
        self.interface_object = interface_object
        self.hsv_filter = {}
        self.get_hsv_filter()
        self.masks = {}
        self.contours = []

    def get_hsv_filter(self):
        """
        define the range for the filter
        Returns:

        """
        lower_white = np.array([0, 0, 70])
        upper_white = np.array([180, 25, 160])

        lower_red = np.array([110, 55, 65])
        upper_red = np.array([135, 255, 255])
        lower_yellow = np.array([80, 150, 100])
        upper_yellow = np.array([105, 255, 255])
        lower_blue = np.array([0, 150, 60])
        upper_blue = np.array([20, 255, 255])
        # lower_blue_2 = np.array([150, 150, 60])
        # upper_blue_2 = np.array([180, 255, 255])
        self.hsv_filter = {'white': (lower_white, upper_white),
                           'red': (lower_red, upper_red),
                           'yellow': (lower_yellow, upper_yellow),
                           'blue': (lower_blue, upper_blue), }

    def extract_shapes(self, frame=None, debug_mode=False):
        """update the gui with the new images"""
        if frame is None:
            frame = self.interface_object.frame_dict['original']
        frame_copy = copy.deepcopy(frame)

        all_mask = self.apply_hsv_color_filter(frame_copy)
        self.interface_object.frame_dict['color_mask'] = all_mask

        all_mask_morphology = morphology_operation(copy.deepcopy(all_mask))
        self.interface_object.frame_dict['color_mask_with_morphology'] = all_mask_morphology

        y_coordinate_to_ignore = int(frame_copy.shape[0] * 0.70)
        all_mask_morphology[y_coordinate_to_ignore:] = 0

        self.get_filtered_contours(all_mask_morphology)
        self.update_patch_objects()

        if debug_mode:
            self.visualization_subprocess()

    def update_patch_objects(self):
        """
        update interface object
        Returns:

        """
        for contour in self.contours:
            pos_x, pos_y, width, height = cv2.boundingRect(contour)
            original_frame = self.interface_object.frame_dict['original']
            patch = original_frame[pos_y: pos_y + height, pos_x: pos_x + width, ::-1]
            self.interface_object.add_patch(patch, [pos_x, pos_y], [width, height])

    def apply_hsv_color_filter(self, frame_copy, debug_mode=False):
        """
        filter the frame in hsv color space based on hand-crafted conditions
        Args:
            frame_copy:
            debug_mode:

        Returns:

        """
        frame_hsv = cv2.cvtColor(frame_copy, cv2.COLOR_RGB2HSV)
        all_mask = np.zeros_like(frame_copy)[..., 0]
        for color, filter_range in self.hsv_filter.items():
            self.masks[color] = cv2.inRange(frame_hsv, filter_range[0], filter_range[1])
            if debug_mode:
                self.interface_object.frame_dict[color] = self.masks[color]
            all_mask |= self.masks[color]
        return all_mask

    def get_filtered_contours(self, all_mask_morphology):
        """
        filter the contours base on some hand-crafted conditions
        Args:
            all_mask_morphology:

        Returns:

        """
        self.contours, hierarchy = cv2.findContours(all_mask_morphology,
                                                    cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.filter_contours_by_hierarchy(hierarchy)
        self.contours = [cv2.approxPolyDP(cnt, 0.05 * cv2.arcLength(cnt, True), True)
                         for cnt in self.contours]
        self.contours = filter_contours_by_edge_number(self.contours, (3, float('inf')))
        self.contours = filter_contours_by_area(self.contours, (500, float('inf')))
        self.contours = filter_contours_by_aspect_ratio(self.contours, (0, 50))

    def filter_contours_by_hierarchy(self, hierarchy):
        """
        delete contours that are inside other contours
        Args:
            hierarchy:

        Returns:

        """
        contour_filtered = []
        try:
            for index, element in enumerate(hierarchy[0]):
                if element[3] == -1:
                    contour_filtered.append(self.contours[index])
        except TypeError:
            pass
        self.contours = contour_filtered

    def visualization_subprocess(self):
        """
        visualization the frame dict for debugging purpose
        Returns:

        """
        orignal_frame_copy = copy.deepcopy(self.interface_object.frame_dict['original'])
        for contour in self.contours:
            pos_x, pos_y, width, height = cv2.boundingRect(contour)
            cv2.rectangle(orignal_frame_copy, (pos_x, pos_y),
                          (pos_x + width, pos_y + height), (0, 0, 255), 3)

        self.interface_object.frame_dict['bounding boxes'] = orignal_frame_copy
        for frame_name, frame in self.interface_object.frame_dict.items():
            if frame_name not in ['orginal', 'default']:
                cv2.imshow(frame_name, frame)
        cv2.waitKey(0)


if __name__ == "__main__":
    PATHS = glob.glob('../../data/test_images/*.jpg')
    _INT_OBJ = InterfaceObject()
    COLOR_ANA = ColorAnalyser(_INT_OBJ)
    for _path in PATHS:
        image = cv2.imread(_path)
        _INT_OBJ.frame_dict['original'] = image
        COLOR_ANA.extract_shapes(image, True)
    for _frame in frame_generator(
            "../../data/youtube_videos/Munich city Drive from South East to South West.mp4",
            {"stop": threading.Event()}):
        COLOR_ANA.extract_shapes(_frame)
