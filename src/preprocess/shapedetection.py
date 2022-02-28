"""preprocessing element: shapedetection"""
import copy
import cv2
from preprocess.preprocess_utils import canny_edge_detector, morphology_operation
from preprocess.preprocess_utils import filter_contours_by_aspect_ratio, filter_contours_by_area
from preprocess.preprocess_utils import filter_contours_by_edge_number


class ShapeDetector:
    """this class detect the geometric shapes with find contour"""

    def __init__(self, interface_object):
        """initialization"""
        self.frame = None
        self.annotate_frame = None

        self.font = cv2.FONT_HERSHEY_COMPLEX
        self.contours = []
        self.bounding_box = []
        self.interface_object = interface_object

    def update_frame(self, frame):
        """update frame object"""
        self.frame = frame
        self.annotate_frame = copy.deepcopy(frame)

    def extract_shapes(self, frame):
        """extract the geometric shapes"""
        self.update_frame(frame)
        self.annotate_frame = cv2.bilateralFilter(self.annotate_frame, 8, 80, 80)
        self.interface_object.frame_dict["blur"] = self.annotate_frame

        self.annotate_frame = cv2.cvtColor(self.annotate_frame, cv2.COLOR_BGR2GRAY)
        self.interface_object.frame_dict["gray"] = self.annotate_frame
        self.annotate_frame = canny_edge_detector(frame)
        self.interface_object.frame_dict["canny"] = self.annotate_frame
        self.annotate_frame = morphology_operation(self.annotate_frame, 1)

        self.contours, _ = cv2.findContours(self.annotate_frame,
                                            cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        self.contours = [cv2.approxPolyDP(cnt, 0.05 * cv2.arcLength(cnt, True), True)
                         for cnt in self.contours]

        self.contours = filter_contours_by_edge_number(self.contours, (3, float('inf')))
        self.contours = filter_contours_by_area(self.contours, (500, float('inf')))
        self.contours = filter_contours_by_aspect_ratio(self.contours, (0, 50))

        self.draw_visualization()

    def draw_visualization(self):
        """draw visualization"""
        for cnt in self.contours:
            cv2.polylines(self.annotate_frame, [cnt], 0, (200), 2)
            pos_x, pos_y, width, height = cv2.boundingRect(cnt)
            # self.bounding_box.append([pos_x, pos_y, width, height])
            patch = self.frame[pos_y: pos_y + height, pos_x:pos_x + width, ::-1]

            self.interface_object.add_patch(patch, [pos_x, pos_y], [width, height])
            # cv2.imshow('patch', patch)
            cv2.rectangle(self.annotate_frame, (pos_x, pos_y),
                          (pos_x + width, pos_y + height), (255), 3)
            pos_x = cnt.ravel()[0]
            pos_y = cnt.ravel()[1]
            if len(cnt) == 3:
                cv2.putText(self.annotate_frame, "Triangle", (pos_x, pos_y), self.font, 1, (255))
            if len(cnt) == 4:
                cv2.putText(self.annotate_frame, "Rectangle", (pos_x, pos_y), self.font, 1, (255))
            if len(cnt) == 8:
                cv2.putText(self.annotate_frame, "Octagon", (pos_x, pos_y), self.font, 1, (255))
            if len(cnt) >= 20:
                cv2.putText(self.annotate_frame, "Circle", (pos_x, pos_y), self.font, 1, (255))
