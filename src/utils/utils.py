"""utils method handling different tasks"""
import cv2


def frame_generator(path, events):
    """Frame Generator
    """

    if str(path).lower().endswith(".mp4") or path == 0:
        # generate the next frame
        cap = cv2.VideoCapture(path)
        frame_id = 0
        while not events['stop'].is_set():
            ret, frame = cap.read()
            if not ret:
                print('no frame left to grab')
                break
            yield frame
            frame_id += 1
        events['stop'].clear()
    else:
        cap = cv2.imread(path)
        yield cap
