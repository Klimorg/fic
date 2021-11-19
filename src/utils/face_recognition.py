import tensorflow as tf
from tensorflow.keras.models import load_model
from omegaconf import OmegaConf

config = OmegaConf.load("src/config.yaml")

model = load_model(config.model_address)


def get_submodel(model, layername, freezed=True):
    """[summary]

    Args:
        model ([type]): [description]
        layername ([type]): [description]
        freezed (bool, optional): [description]. Defaults to True.

    Returns:
        [type]: [description]
    """

    layer_name = layername
    submodel = tf.keras.Model(inputs=model.input,
                              outputs=model.get_layer(layer_name).output)

    if freezed:
        for layer in submodel.layers:
            layer.trainable = False

    return submodel

def classify(img):

    img = tf.reshape(img, (-1, 224, 224, 3))

    return model.predict(img)
