import numpy
import tensorflow as tf

IMAGE_SHAPE = (256, 256, 3)


class Wrapper(tf.keras.Model):
    def __init__(self, base_model):
        super(Wrapper, self).__init__()

        self.base_model = base_model
        self.average_pooling_layer = tf.keras.layers.AveragePooling2D(name="polling")
        self.flatten = tf.keras.layers.Flatten(name="flatten")
        self.dense = tf.keras.layers.Dense(64, activation="relu")
        self.dropout = tf.keras.layers.Dropout(0.5)
        self.output_layer = tf.keras.layers.Dense(2, activation="softmax")

    def call(self, inputs):
        x = self.base_model(inputs)
        x = self.average_pooling_layer(x)
        x = self.flatten(x)
        x = self.dense(x)
        x = self.dropout(x)
        output = self.output_layer(x)
        return output


def get_densenet_covid_model():
    base_learning_rate = 0.0001
    dense_net = tf.keras.applications.densenet.DenseNet201(input_shape=IMAGE_SHAPE, include_top=False, weights='imagenet')
    dense_net.trainable = False
    dense = Wrapper(dense_net)
    dense.compile(optimizer=tf.keras.optimizers.Adam(lr=base_learning_rate),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return dense


dense_model_covid = get_densenet_covid_model()
#dense_model.load_weights('./scandetector/weights/covid/ae_dense_covid_0503.h5')


def calc_covid_prob(img_batch):
    original_pil_img = img_batch[0]
    numpy_img = numpy.array(original_pil_img)
    img = tf.convert_to_tensor(value=numpy_img)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.image.resize(img, [IMAGE_SHAPE[0], IMAGE_SHAPE[1]])
    img_tensor = tf.expand_dims(img, 0)
    model_output = dense_model_covid.predict(img_tensor)[0][0]
    return model_output
