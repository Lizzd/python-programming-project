"""test bing_image_downloader
"""
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
from utils import bing_image_downloader


def test_bing_image_downloader():
    """test bing_image_downloader:
        1) new directory exists
        2) it is filled with more than 0 images
        3) all images are loadable into numpy and have a reasonable shape
    """
    search_input = "130 kmh schild autobahn"
    limit = 5
    dir_path = bing_image_downloader(search_input, limit)

    assert os.path.exists(dir_path)
    im_files = os.listdir(dir_path)
    assert len(im_files) > 0
    for im_file in im_files:
        image_plt = plt.imread(dir_path / im_file)
        image = np.array(image_plt)
        x_dim, y_dim, z_dim = np.shape(image)
        assert z_dim in (3, 4)
        assert x_dim > 50
        assert y_dim > 50
    shutil.rmtree(dir_path)
