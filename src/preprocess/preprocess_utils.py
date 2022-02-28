"""utils"""
import cv2
import numpy as np


def canny_edge_detector(frame):
    """canny edge detector"""
    median = np.median(frame)
    sigma = 0.33
    lower = int(max(0, (1.0 - sigma) * median))
    upper = int(min(255, (1.0 + sigma) * median))
    frame = cv2.Canny(frame, lower, upper)
    return frame


def morphology_operation(frame, filter_size=3):
    """morphology operation
    currently doing nothing"""
    kernel = np.ones((filter_size, filter_size), np.uint8)
    frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    frame = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)
    return frame


def normalize_image(self):
    """return image patches with a fix size """
    return self.frame


def filter_contours_by_edge_number(contours, allowed_edges_nummber=(3, 10)):
    """filter the hulls with certain conditions"""
    contours = [cnt for cnt in contours
                if allowed_edges_nummber[0] <= len(cnt) <= allowed_edges_nummber[1]]
    return contours


def filter_contours_by_aspect_ratio(contours, aspect_ratio_range=(25, 100)):
    """filter the hulls with certain conditions"""
    contours = [cnt for cnt in contours
                if aspect_ratio_range[0] <=
                (cv2.arcLength(cnt, True) ** 2 / cv2.contourArea(cnt))
                <= aspect_ratio_range[1]]
    return contours


def filter_contours_by_area(contours, area_range=(25, 200)):
    """filter the hulls with certain conditions"""
    contours = [cnt for cnt in contours
                if area_range[0] <= cv2.contourArea(cnt) <= area_range[1]]
    return contours
