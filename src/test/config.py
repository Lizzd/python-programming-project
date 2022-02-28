"""intialize global variable"""
import os
import glob
import cv2

ROOT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..' + os.sep + '..')
DATA_DIR_PATH = os.path.join(ROOT_PATH, 'data')
YOUTUBE_DIR_PATH = os.path.join(DATA_DIR_PATH, 'youtube_videos')
TEST_IMAGES_PATH = os.path.join(DATA_DIR_PATH, 'test_images')
ICONS_PATH = os.path.join(DATA_DIR_PATH, 'icons')

DIRECTORIES_PATH = {'root': ROOT_PATH, 'data': DATA_DIR_PATH, 'youtube': YOUTUBE_DIR_PATH,
                    'test_image': TEST_IMAGES_PATH, 'icons': ICONS_PATH}

TEST_IMAGE_1 = cv2.imread(os.path.join(DATA_DIR_PATH, 'sign_ok.jpg'))
TEST_IMAGE_2 = cv2.imread(os.path.join(DATA_DIR_PATH, 'sign_not_1.jpg'))
TEST_IMAGE_3 = cv2.imread(os.path.join(DATA_DIR_PATH, 'sign_right.jpg'))

TEST_IMAGE_PATHS = glob.glob(os.path.join(TEST_IMAGES_PATH, '*.jpg'))[:3]

print(ROOT_PATH)
