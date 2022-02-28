"""this class handles the visualization tasks"""
import copy
from cv2 import cv2
import numpy


# pylint: disable=too-many-instance-attributes


class Visualizer():
    """this class handles the visualization tasks"""

    def __init__(self, interface_object=None):
        """initalization"""
        self.patch_and_icon_list = []  # max 3 elements
        self.interface_object = interface_object
        self.frame = None
        self.patch_list = None
        self.icon_list = None
        if interface_object is not None:
            self.visualizer = interface_object.command_object.visualizer
        self.cut_size_x = 75
        self.cut_size_y = 15

    def reset_instances(self):
        """

        Returns:

        """
        self.patch_and_icon_list = []  # max 3 elements

    def process(self):
        """

        Args:


        Returns:

        """
        self.reset_instances()
        self.frame = copy.deepcopy(self.interface_object.frame_dict['original'])
        self.type_choose()
        max_patch_to_show = self.interface_object.command_object.visualizer['nr_of_patches']
        visualization_object = self.interface_object.visualization_object
        self.patch_and_icon_list = self.patch_and_icon_list[:max_patch_to_show]
        visualization_object.patch_and_icon_list = self.patch_and_icon_list[:max_patch_to_show]
        visualization_object.final_annotated_frame = self.frame
        self.interface_object.command_object.command_info['start_gui_video'] = True

    def type_choose(self):
        """
        :return:
        """
        # if self.interface_object.frame_dict:  # draw frame type
        frame_list = self.interface_object.get_list_from_frame_dict()
        max_index = len(frame_list) - 1
        if self.visualizer['index_of_frame_dict'] == 1:
            self.frame = self.draw_to_frame()
        elif self.visualizer['index_of_frame_dict'] <= max_index:  # original type
            self.frame = frame_list[self.visualizer['index_of_frame_dict']][1]
        else:
            self.frame = frame_list[max_index][1]
        self.combination_to_patch_and_icon_list()

    def combination_to_patch_and_icon_list(self):
        """:arg"""
        patch_list = self.interface_object.important_patches
        icon_list = self.interface_object.icon_list

        for index, patch in enumerate(patch_list):

            patch_icon_size = (250, 250)
            resize_patch = cv2.resize(patch, patch_icon_size,
                                      interpolation=cv2.INTER_CUBIC)
            resize_icon = cv2.resize(icon_list[index], patch_icon_size,
                                     interpolation=cv2.INTER_CUBIC)

            patch_and_icon = cv2.hconcat([resize_patch, resize_icon])
            if len(self.patch_and_icon_list) <= index:
                self.patch_and_icon_list.append(patch_and_icon)
            elif len(self.patch_and_icon_list) > index:
                self.patch_and_icon_list[index](patch_and_icon)

    def draw_to_frame(self):
        """draw the bounding boxes with opencv"""
        for patch in self.interface_object.patches_list:
            pos_x, pos_y = patch.position
            width, height = patch.size
            translation_pos_y = pos_y + height - 5
            translation_pos_y = translation_pos_y if translation_pos_y > 0 else 0
            translation_pos_x = pos_x
            string_pos_y = pos_y + height - 20
            string_pos_y = string_pos_y if string_pos_y > 0 else 0
            string_pos_x = pos_x
            if self.visualizer['bounding_box']:
                self.draw_bounding_box(pos_x, pos_y, width, height)
            if self.visualizer['show_strings']:
                class_strings = patch.class_strings
                self.draw_strings_to_frame(class_strings, string_pos_x, string_pos_y)
                src_string = patch.translation_info['src_string']
                translation = patch.translation_info['translation']
                ocr_string = f'{src_string}, {translation}'
                self.draw_translation_to_frame(ocr_string, translation_pos_x, translation_pos_y)

        return self.frame

    def draw_bounding_box(self, pos_x, pos_y, width, height):
        """:var"""
        cv2.rectangle(self.frame, (pos_x, pos_y), (pos_x + width, pos_y + height),
                      (255, 0, 0), 1)

    def draw_strings_to_frame(self, class_strings, string_pos_x, string_pos_y):
        """:arg
        """
        color_strings = self.compute_best_fg_color_for_the_strings_text(string_pos_x, string_pos_y)
        cv2.putText(self.frame, class_strings,
                    (string_pos_x, string_pos_y),
                    cv2.FONT_HERSHEY_PLAIN, 1,
                    color_strings, 1)

    def draw_translation_to_frame(self, translation, translation_pos_x, translation_pos_y):
        """:var"""

        color_translation = self.compute_best_fg_color_for_the_translation_text(translation_pos_x,
                                                                                translation_pos_y)

        cv2.putText(self.frame, translation,
                    (translation_pos_x, translation_pos_y),
                    cv2.FONT_HERSHEY_PLAIN, 1, color_translation, 1)

    def compute_best_fg_color_for_the_strings_text(self, string_pos_x, string_pos_y):
        """:arg"""
        string_pos_y_shift = string_pos_y - 15
        string_pos_y_shift = string_pos_y_shift if string_pos_y_shift > 0 else 0
        cut_image_for_color = self.frame[string_pos_y_shift:string_pos_y_shift + self.cut_size_y,
                                         string_pos_x:string_pos_x + self.cut_size_x
                                         ]
        color_strings_invert_row = numpy.average(cut_image_for_color, axis=0)
        color_strings_invert = numpy.average(color_strings_invert_row, axis=0)
        color_strings_invert = int((numpy.average(color_strings_invert, axis=0) + 127) % 255)
        color_strings = [color_strings_invert for _ in range(3)]
        return tuple(color_strings)

    def compute_best_fg_color_for_the_translation_text(self, translation_pos_x, translation_pos_y):
        """

        Returns:

        """
        translation_pos_y_shift = translation_pos_y - 15
        translation_pos_y_shift = translation_pos_y_shift if translation_pos_y_shift > 0 else 0
        cut_image_for_color = self.frame[translation_pos_y_shift: translation_pos_y_shift +
                                         self.cut_size_y,
                                         translation_pos_x:translation_pos_x +
                                         self.cut_size_x]
        color_translation_invert_row = numpy.average(cut_image_for_color, axis=0)
        color_translation_invert = numpy.average(color_translation_invert_row, axis=0)
        color_translation_invert = int(
            (numpy.average(color_translation_invert, axis=0) + 127) % 255)
        color_translation = [color_translation_invert for _ in range(3)]
        return tuple(color_translation)


class Examine():
    """:arg"""

    def __init__(self):
        self.string_pos = [100, 730]
        self.translation_pos = [100, 745]
        self.pos = [100, 70]
        self.size = [750, 680]
        self.visualizer = Visualizer()
        self.cut_size_translation = self.visualizer.cut_size_y
        self.cut_size_string = self.visualizer.cut_size_y
        self.visualizer.patch_list = [cv2.imread('sign_right.jpg')]
        self.visualizer.frame = cv2.imread('sign_right.jpg')
        self.visualizer.icon_list = [self.visualizer.frame]

    def test_bounding_box(self):
        """:arg"""

        self.visualizer.frame = cv2.imread('sign_right.jpg')
        self.visualizer.draw_bounding_box(self.pos[0], self.pos[1], self.size[0], self.size[1])
        cv2.imshow('image1', self.visualizer.frame)
        cv2.waitKey(0)

    def test_draw_strings_and_translation(self):
        """:arg"""
        self.visualizer.draw_strings_to_frame("test strings", self.string_pos[0], self.string_pos[1]
                                              )
        self.visualizer.draw_translation_to_frame("test translation", self.translation_pos[0],
                                                  self.translation_pos[1])
        cv2.imshow('image2', self.visualizer.frame)
        cv2.waitKey(0)


def test_process():
    """:arg"""
    test = Examine()
    test.test_bounding_box()
    test.test_draw_strings_and_translation()


if __name__ == '__main__':
    test_process()
