# Report regarding the current model and results
## by Razvan-Mihai Ursu @ge36daj
### Date: 27.05.2020

[Original Repository](https://github.com/naokishibuya/car-traffic-sign-classification)

#### Update 29.05.2020
I have created a minimal_test.py file, which can just let network10 evaluate the pictures. However, for the classification we will also need the preprocessors:
```python
loader = lambda image_file: resize_image(load_image(image_file))
normalizer = lambda x: (x - x.mean())/x.std()
augmenter = lambda x: x


preprocessors = [loader, augmenter, normalizer]
```
It works very well, but I feel that we could eliminate the pipeline and convert the .ckpt file to a regular .pb and work with the model in that format. However, this is something we should work on only if the performance of the evaluation is not quick enough, which at this point I highly doubt.

A more important point would be to find an algorithm able to extract ROIs (Regions of Interest) which could possibly contain such street signs.

If you want to test yourself the evaluation, you can find in this folder 2 pictures ([sign_roundabout.jfif](sign_roundabout.jfif) and [sign_right.jpg](sign_right.jpg)). Please note that the original random images (not in this repo) do not appear to work, as they seem to have 4 channels, and not 3 (RGB).


#### Original
The results of the model seem to be pretty good. The model was trained on the GTRSB dataset and the best of it (network10) has an accuracy of 95% on the Final_Test dataset, however in the case of random images, as the author also suggests, the accuracy could be lower (such as 70%).

Moreover, the author suggests: *"Therefore, we will need an object recognition mechanism that scan across the image with sliding windows to find the candidate signs. This kind of detection mechanism is not covered in this project."*

In this case we should also consider searching for such an object detection algorithm.

The GTRSB dataset can be downloaded from: https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/published-archive.html.
If you want to retrain the model, you should download:
- GTSRB_Final_Test_Images.zip
- GTSRB_Final_Training_Images.zip
- GTSRB_Final_Test_GT.zip - containing a .csv file with the labels of the GTSRB_Final_Test_Images

I have already trained the most accurate networks, with results almost identical to that of the author. The checkpoint files can be found in /checkpoint. For an example how to restore and test the model please see below:

```python
with Session() as session:
    pipeline = build_pipeline(preprocessors, session, make_network3())
    session.load('checkpoint/network10.ckpt')
    score = pipeline.score(X_test, y_test)
    print('Test Score: {}'.format(score))
```
The code uses Tensorflow v1 so I had to adapt the code in a few places for the new Tensorflow v2.2.0.

For further details please see the Traffic_Sign_Classifier.ipynb as well as the ORIGINAL_README.

@ga27yug @ge56luh @ga27bup