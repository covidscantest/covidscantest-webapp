import numpy
import tensorflow as tf
from .utils import create_model

IMAGE_SHAPE = (320, 320, 3)

pretrined_densenet = tf.keras.applications.densenet.DenseNet201(include_top=False, weights='imagenet', input_tensor=None,
                                                              input_shape=IMAGE_SHAPE, pooling=None, classes=1000)
pretrined_densenet.trainable = False
densenet_model_healthy = create_model(pretrined_densenet)
densenet_model_healthy.load_weights('./scandetector/weights/healthy/as_densenet201_healthy_0503_1.h5')


def calc_healthy_prob(tf_image):
    img = tf.image.resize(tf_image, [IMAGE_SHAPE[0], IMAGE_SHAPE[1]])
    img_tensor = tf.expand_dims(img, 0)
    model_output = densenet_model_healthy.predict(img_tensor)[0][0]
    return model_output
