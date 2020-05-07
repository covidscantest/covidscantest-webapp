import tensorflow as tf

def create_model(pretrined_model):
    base_learning_rate = 0.0001
    pretrined_model.trainable = False
    current_layer = pretrined_model.output
    current_layer = tf.keras.layers.AveragePooling2D()(current_layer)
    current_layer = tf.keras.layers.Flatten()(current_layer)
    current_layer = tf.keras.layers.Dense(64, activation="relu")(current_layer)
    current_layer = tf.keras.layers.Dropout(0.5)(current_layer)
    current_layer = tf.keras.layers.Dense(2, activation="softmax")(current_layer)

    our_model = tf.keras.models.Model(inputs=pretrined_model.input, outputs=current_layer)

    our_model.compile(optimizer=tf.keras.optimizers.Adam(lr=base_learning_rate),
                      loss='binary_crossentropy', metrics=['accuracy'])
    return our_model