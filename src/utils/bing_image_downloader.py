"""
download images found on www.bing.com/images
"""
from pathlib import Path
import urllib.request
import urllib
import re
import http


def bing_image_downloader(search_input, limit):
    """download images found on www.bing.com/images

    Args:
        search_input (String): key words for internet search
        limit (int): maximum number of images to download

    Returns:
        (String): path to directory where images are downloaded into
    """
    a_path = Path(__file__).resolve().parent.parent.parent
    dir_path = a_path / "data" / "internet_image_downloader" / search_input
    i = 2
    while dir_path.exists():
        dir_path = dir_path.parent / (search_input + "_" + str(i))
        i += 1
    dir_path.mkdir(parents=True)

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
    }
    request_url = 'https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(search_input) \
                  + '&first=0&count=' + str(limit) + '&adlt=True&qft='

    try:
        request = urllib.request.Request(request_url, None, headers=headers)
        response = urllib.request.urlopen(request)
    except urllib.error.URLError:
        return 0
    html = response.read().decode('utf8')
    links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)

    i = 1
    for link in links:
        file_path = dir_path / ("Image_" + str(i) + ".jpg")
        flag = link_image_downloader(link, file_path, headers)
        if flag:
            print(str(i) + " image/s downloaded")
            i += 1
    return dir_path


def link_image_downloader(link, file_path, headers):
    """download image from link

    Args:
        link (String): link where image can be found
        file_path (String): path where image shall be stored (without ".jpg")

    Returns:
        (bool): image was downloadable
    """
    request = urllib.request.Request(link, None, headers)
    try:
        jpg = urllib.request.urlopen(request).read()
        with open(file_path, 'wb') as f_p:
            f_p.write(jpg)
        return True
    except (urllib.error.URLError, UnicodeEncodeError, http.client.InvalidURL):
        return False
