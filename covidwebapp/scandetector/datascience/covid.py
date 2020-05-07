import numpy
import tensorflow as tf
from .utils import create_model

IMAGE_SHAPE = (224, 224, 3)

pretrined_densenet = tf.keras.applications.densenet.DenseNet201(input_shape=IMAGE_SHAPE, include_top=False, weights='imagenet')
pretrined_densenet.trainable = False
dense_model_covid = create_model(pretrined_densenet)
dense_model_covid.load_weights('./scandetector/weights/covid/ae_densenet201_covid_0504.h5')


def calc_covid_prob(tf_image):
    img = tf.image.resize(tf_image, [IMAGE_SHAPE[0], IMAGE_SHAPE[1]])
    img_tensor = tf.expand_dims(img, 0)
    model_output = dense_model_covid.predict(img_tensor)[0][0]
    return model_output
