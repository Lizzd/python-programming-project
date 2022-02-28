"""Recorder Class"""

from datetime import datetime
import cv2


class Recorder:
    """Recorder Class
    """

    def __init__(self):
        self.original_path = None
        self.is_recording = False

        self.size = (960, 540)
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.fps = 25
        self.recorder = None

    def save(self):
        """Save
        """
        self.recorder.release()
        self.is_recording = False

    def write(self, image):
        """Write an image to the video

        Args:
            image (ndarray): A frame of the video to be captured
        """
        self.recorder.write(image)

    def start_recording(self, original_path):
        """Start_recording
        """
        recording_name = datetime.now().strftime("%d_%m_%Y_%H%M%S")
        extension = ".mp4"
        path = recording_name + extension

        self.original_path = original_path

        self.recorder = cv2.VideoWriter(path, self.fourcc, self.fps, self.size)
        self.is_recording = True
