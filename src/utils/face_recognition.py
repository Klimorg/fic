import tensorflow as tf
from tensorflow.keras.models import load_model

model = load_model("src/models/face_recogFIC.h5")


def classify(img):

    img = tf.reshape(img, (-1, 224, 224, 3))

    return model.predict(img)
