"""Test the performance of classifer2 and/or classifier_combination
    -images are dowloaded from the internet
    -these images are put into the right format (interface_object)
    -the classifier predicts their classes
    -assert accuracy > threshhold
"""
import shutil
from pathlib import Path
import imageio
from classifier import ClassifierCombination
from objects import InterfaceObject
from utils import bing_image_downloader


def create_interface_object(sign_name, number):
    """ returns images from the internet as the format needed for the classifier

    Args:
        sign_name (String): [description]
        number (int): [description]

    Returns:
        InterfaceObject: the input format for the classifier
    """
    dir_path = bing_image_downloader(sign_name, number)
    path_list = Path(dir_path).glob('**/*')
    interface_object = InterfaceObject()
    for path in path_list:
        try:
            pic = imageio.imread(path)
            if pic.shape[2] == 3:
                interface_object.add_patch(pic, [0, 0], [0, 0])
        except ValueError:
            pass
    shutil.rmtree(dir_path)
    return interface_object


def test_classifier_combination():
    """Test the performance of classifer2 and/or classifier_combination
    -example images are dowloaded from the internet
    -these images are put into the right format (interface_object)
    -the classifier predicts their classes
    -assert accuracy > threshhold
    """
    number_of_tests_per_class = 5
    test_sign_classes = [
        ["30 kmh schild geschwindigkeitsbegrenzung", 1],
        ["100 kmh schild geschwindigkeitsbegrenzung", 7],
        ["120 kmh schild geschwindigkeitsbegrenzung", 8],
        ["kreisverkehr schild deutschland", 40]]

    total_classifications = 0
    right_classifications = 0

    for sign_class in test_sign_classes:
        sign_name, label = sign_class
        interface_object = create_interface_object(sign_name, number_of_tests_per_class)
        classifier = ClassifierCombination(interface_object)
        classifier.predict_proba()

        for patch in interface_object.patches_list:
            probabilities = list(patch.probabilities)
            max_value = max(probabilities)
            max_index = probabilities.index(max_value)

            total_classifications += 1
            if max_index == label:
                right_classifications += 1

    print("total_classifications: " + str(total_classifications))
    print("right_classifications: " + str(right_classifications))
    print("right_classifications / total_classifications: " + str(
        right_classifications / total_classifications))

    assert total_classifications > 0
    assert right_classifications / total_classifications > 0.3
