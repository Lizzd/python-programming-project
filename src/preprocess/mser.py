"""preprocessing element: MSER"""

import copy
import cv2
import numpy as np


class MSER:
    """ use MSER (Maximally stable extremal regions) to detect signs on the frame"""

    def __init__(self, interface_object):
        """initialization"""
        self.frame = None
        self.annotate_frame = None
        self.mask = None

        self.interface_object = interface_object
        self.mser = cv2.MSER_create()

        self.mode = 'polylines'
        self.hulls = []

    def update_frame(self, _frame):
        """update frame object"""
        self.frame = _frame
        self.annotate_frame = copy.deepcopy(_frame)

    def extract_shapes(self, _frame):
        """apply the mser onto the frame """
        self.update_frame(_frame)
        self.annotate_frame = cv2.bilateralFilter(self.annotate_frame, 8, 80, 80)
        self.interface_object.frame_dict["blur"] = self.annotate_frame
        self.annotate_frame = cv2.cvtColor(self.annotate_frame, cv2.COLOR_BGR2GRAY)
        self.interface_object.frame_dict["gray"] = self.annotate_frame

        regions_pointsets, _bounding_box = self.mser.detectRegions(self.annotate_frame)
        self.hulls = [cv2.convexHull(point.reshape(-1, 1, 2)) for point in regions_pointsets]
        self.filter_hulls_by_edge_number()
        self.filter_hulls_by_area()

        for hull in self.hulls:
            pos_x, pos_y, width, height = cv2.boundingRect(hull)
            patch = self.frame[pos_y: pos_y + height, pos_x:pos_x + width, ::-1]
            self.interface_object.add_patch(patch, [pos_x, pos_y], [width, height])

        if self.mode == 'polylines':
            self.draw_polylines()
            self.interface_object.frame_dict["polylines"] = self.annotate_frame
        elif self.mode == 'mask':
            self.create_mask()
            self.draw_mask()

        # self.visualize_process()
        self.interface_object.annotate_frame = self.annotate_frame

    def draw_mask(self):
        """draw the mask onto the frame"""
        self.annotate_frame = cv2.bitwise_and(self.annotate_frame,
                                              self.annotate_frame, mask=self.mask)

    def create_mask(self):
        """create the mask """
        self.mask = np.zeros((self.frame.shape[0], self.frame.shape[1], 1), dtype=np.uint8)
        for contour in self.hulls:
            cv2.drawContours(self.mask, [contour], -1, (255, 255, 255), -1)

    def draw_polylines(self):
        """draw the polylines around the object of interest"""
        self.annotate_frame = cv2.polylines(self.frame.copy(), self.hulls, 1, (0, 255, 0))

    def filter_hulls_by_edge_number(self, allowed_edges_nummber=(3, 10)):
        """filter the hulls with certain conditions"""
        self.hulls = [cnt for cnt in self.hulls
                      if allowed_edges_nummber[0] <= len(cnt) <= allowed_edges_nummber[1]]

    def filter_hulls_by_perimeter(self, perimeter_range=(25, 100)):
        """filter the hulls with certain conditions"""
        self.hulls = [cnt for cnt in self.hulls
                      if perimeter_range[0] <= cv2.arcLength(cnt, True) <= perimeter_range[1]]

    def filter_hulls_by_area(self, area_range=(25, 200)):
        """filter the hulls with certain conditions"""
        self.hulls = [cnt for cnt in self.hulls
                      if area_range[0] <= cv2.contourArea(cnt) <= area_range[1]]

    def visualize_process(self):
        """visualize the annotated frame with opencv"""
        cv2.imshow('annotated frame mser', self.annotate_frame)
