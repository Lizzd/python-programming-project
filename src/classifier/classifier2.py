"""an lternative to our original classifier but with keras
"""
from pathlib import Path
import glob
import keras
import numpy as np
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


class Classifier2():
    """ classify sign images into one of 42 classes / give probability for every class
    Difference to Classifier(1): slightly different layer structure and different
    cost function for training
    """

    def __init__(self, interface_object=None):
        """

        Args:
            interface_object:
        """
        self.interface_object = interface_object
        self.number_of_classes = 43
        self.cnn = None
        self.cnn_created = False
        highest_path = Path(__file__).resolve().parent.parent.parent
        self.weights_path = highest_path / "data" / "classifier2_weights" / "my_model_weights.h5"

    def predict_proba(self):
        """ This function generates the array of probabilities,
            based on the interface_object and saves them in the
            interface_object.patches_list[i].probabilities.
        """

        if not self.cnn_created:
            self.cnn = self.create_cnn()
            self.cnn.load_weights(str(self.weights_path))
            self.cnn_created = True

        if self.interface_object.patches_list:
            images = np.array([
                cv2.resize(
                    patch.patch, (32, 32), interpolation=cv2.INTER_CUBIC
                    )
                / 255 for patch in self.interface_object.patches_list])

            prob_list = self.cnn.predict(images)

            for patch, prob in zip(self.interface_object.patches_list, prob_list):
                patch.probabilities = prob

    def train(self, max_epoch=10, continue_training=False):
        """

        Args:
            max_epoch:
            continue_training:

        Returns:

        """
        cnn = self.create_cnn()
        if continue_training:
            cnn.load_weights("src/classifier2/my_model_weights.h5")

        images = np.load("src/classifier2/img.npy")
        images = images / np.max(images)
        labels = np.load("src/classifier2/lbl.npy")

        print(images.shape)
        print(labels.shape)

        cnn.fit(images, labels, epochs=max_epoch, batch_size=4000, verbose=1)
        cnn.save_weights('my_model_weights_2.h5')

    def test(self):
        """

        Returns:

        """
        cnn = self.create_cnn()
        cnn.load_weights(str(self.weights_path))

        images_val = np.load("src/classifier2/img_val.npy")
        images_val = images_val / np.max(images_val)

        pred = cnn.predict(images_val)

        for i in range(images_val.shape[0]):
            print("3 most likly classes: ")
            for j in range(3):
                max_index = pred[i].argmax()
                max_value = pred[i].max()
                print(
                    str(j + 1) + ") class: " + str(max_index) + "   propability: " + str(max_value))
                pred[i, max_index] = -1
            plt.imshow(images_val[i])
            plt.show()

    def create_cnn(self):
        """

        Returns:

        """
        cnn = keras.models.Sequential()
        cnn.add(keras.layers.Conv2D(24, kernel_size=(5, 5),
                                    activation='relu',
                                    input_shape=(32, 32, 3)))
        cnn.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
        cnn.add(keras.layers.Conv2D(64, (5, 5), activation='relu'))
        cnn.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
        cnn.add(keras.layers.Dropout(0.5))
        cnn.add(keras.layers.Flatten())
        cnn.add(keras.layers.Dense(480, activation='relu'))
        cnn.add(keras.layers.Dense(self.number_of_classes, activation='sigmoid'))

        cnn.compile(loss=keras.losses.binary_crossentropy,  # categorical_crossentropy,
                    optimizer=keras.optimizers.Adam(learning_rate=0.001),  # 0.0001, 20 eps
                    metrics=['accuracy', ])  # keras.metrics.Precision()])
        return cnn

    def load_images(self):
        """

        Returns:

        """
        image_size = 32
        images = np.zeros((1, image_size, image_size, 3))
        labels = np.zeros((1, self.number_of_classes))
        for i in range(self.number_of_classes):
            print(i)
            for im_path in glob.glob(
                    "/home/korte/Desktop/pypro/sign_pictures/Val/" + str(i) + "/*.png"):
                image = mpimg.imread(im_path)
                image = cv2.resize(
                    image, dsize=(image_size, image_size), interpolation=cv2.INTER_CUBIC) / 255
                print(image.shape)
                images = np.concatenate((images, np.array([image[:, :, :3]])), axis=0)
                label = np.zeros((self.number_of_classes))
                label[i] = 1
                labels = np.concatenate((labels, np.array([label])), axis=0)
        print(images[1:].shape)
        print(labels[1:].shape)
        images = images[1:]
        labels = labels[1:]
        np.save("src/classifier2/img_val.npy", images)
        np.save("src/classifier2/lbl_val.npy", labels)
