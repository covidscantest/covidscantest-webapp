import numpy
import tensorflow as tf
IMAGE_SHAPE = (320, 320, 3)

def create_model(layers_to_freeze, pretrained_model):
    base_learning_rate = 0.0001
    current_layer = pretrained_model.output
    current_layer = tf.keras.layers.Flatten()(current_layer)
    current_layer = tf.keras.layers.Dense(units=500, activation='tanh')(current_layer)
    current_layer = tf.keras.layers.Dropout(rate=0.33)(current_layer)
    current_layer = tf.keras.layers.Dense(units=250, activation='tanh')(current_layer)
    current_layer = tf.keras.layers.Dense(units=120, activation='tanh')(current_layer)
    current_layer = tf.keras.layers.Dropout(rate=0.33)(current_layer)
    current_layer = tf.keras.layers.Dense(units=50, activation='tanh')(current_layer)
    current_layer = tf.keras.layers.Dense(units=2, activation='softmax')(current_layer)

    our_model = tf.keras.models.Model(inputs=pretrained_model.input, outputs=current_layer)

    for layer in our_model.layers[:layers_to_freeze]:
        layer.trainable = False
    for layer in our_model.layers[layers_to_freeze:]:
        layer.trainable = True

    our_model.compile(optimizer=tf.keras.optimizers.Adam(lr=base_learning_rate),
                      loss='binary_crossentropy', metrics=['accuracy'])
    return our_model


pretrined_densenet = tf.keras.applications.densenet.DenseNet201(include_top=False, weights='imagenet', input_tensor=None,
                                                              input_shape=IMAGE_SHAPE, pooling=None, classes=1000)

densenet_model_pneumo = create_model(4, pretrined_densenet)
densenet_model_pneumo.load_weights('./scandetector/weights/pneumonia/as_densenet201_pneumonia_0502.h5')

def calc_pneumo_prob(img_batch):
    original_pil_img = img_batch[0]
    numpy_img = numpy.array(original_pil_img)
    img = tf.convert_to_tensor(value=numpy_img)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.image.resize(img, [IMAGE_SHAPE[0], IMAGE_SHAPE[1]])
    img_tensor = tf.expand_dims(img, 0)
    model_output = densenet_model_pneumo.predict(img_tensor)[0][0]
    return model_output