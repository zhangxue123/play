"""
Classify a few images through our CNN.
"""
import numpy as np
from processor import process_image
from keras.models import load_model
from keras import backend as K
import matplotlib.pyplot as plt
import cv2

def main():
    model = load_model('inception.026-1.07.hdf5') #replaced by your model name
    # Get all our test images.
    image='r.jpg'
    images=cv2.imread('r.jpg')
    #cv2.imshow("Image", images)
    #cv2.waitKey(0)
    # Turn the image into an array.
    image_arr = process_image(image, (299, 299, 3))
    image_arr = np.expand_dims(image_arr, axis=0)

    layer_1 = K.function([model.layers[0].input], [model.layers[1].output])
    f1 = layer_1([image_arr])[0]
    for _ in range(32):
        show_img = f1[:, :, :, _]
        show_img.shape = [149, 149]
        plt.subplot(4, 8, _ + 1)
        plt.subplot(4, 8, _ + 1)
        plt.imshow(show_img, cmap='gray')
        plt.axis('off')
    plt.show()
    # conv layer: 299
    layer_1 = K.function([model.layers[0].input], [model.layers[299].output])
    f1 = layer_1([image_arr])[0]
    for _ in range(81):
        show_img = f1[:, :, :, _]
        show_img.shape = [8, 8]
        plt.subplot(9, 9, _ + 1)
        plt.imshow(show_img, cmap='gray')
        plt.axis('off')

    plt.show()
    print('This is the end !')

if __name__ == '__main__':
    main()
