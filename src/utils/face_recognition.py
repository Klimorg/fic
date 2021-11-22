import tensorflow as tf
from tensorflow.keras.models import load_model
from omegaconf import OmegaConf
import streamlit as st

config = OmegaConf.load("src/config.yaml")



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


@st.cache(allow_output_mutation=True)
def get_models():

    model = load_model(config.model_address)
    logit_model = get_submodel(model, 'logits')
    embd_model = get_submodel(model, 'Embedding_3')

    return model, logit_model, embd_model

def classify(model, img):

    img = tf.reshape(img, (-1, 224, 224, 3))

    return model.predict(img)
