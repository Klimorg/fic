import numpy as np
import streamlit as st
from PIL import Image
import tensorflow as tf
from utils.align_faces import extract_face
from utils.face_recognition import classify, get_models
from utils.video_capture import capture
# from cleverhans.future.tf2.attacks import projected_gradient_descent as pgd
# from cleverhans.tf2.attacks.projected_gradient_descent import projected_gradient_descent
# from cleverhans.tf2.attacks.fast_gradient_method import fast_gradient_method

from utils.attacks import projected_gradient_descent as pgd

st.header("Démonstrateur Attaque antagoniste CITC !")

model, logit_model, embd_model = get_models()

capture()

st.sidebar.title("Reconnaissance faciale.")

align = extract_face("src/saved_frames/test.jpg")

if st.sidebar.button("Lancer", key="face_recog"):
    y_hat = classify(model, align)

    if (np.argmax(y_hat) == 6) and (1 - np.max(y_hat) <= 0.05):
        st.image(align, channels="RGB")
        st.success("PERSONNE AUTORISEE")
    else:
        st.image(align, channels="RGB")
        st.error("PERSONNE INCONNUE")


st.sidebar.title("Paramètres de l'attaque.")

eps = st.sidebar.number_input("Force du bruit", key="eps", min_value=0.025, value=0.025)
eps_iter = st.sidebar.number_input("Bruit itératif", key="eps_iter", min_value=0.02, value=0.02)
nb_iter = st.sidebar.number_input("Nombre total d'itération", key="nb_iter", min_value=1, value=30)
target = st.sidebar.number_input("Personne à cibler", key="target", min_value=1, max_value=6, value=6)

st.info(f"{type(eps)}")

if st.button("Attaque"):

    adv_img = Image.open("src/aligned_frames/test.jpg")
    adv_img = tf.image.convert_image_dtype(adv_img, tf.float32)
    adv_img = tf.image.resize(adv_img, [224, 224])
    # reshape it with batch size 1 for inference
    st.image(adv_img.numpy(), clamp=True)
    adv_img = tf.reshape(adv_img, (-1, 224, 224, 3))
    

    noise = pgd(logit_model,
                    adv_img,
                    eps=float(eps),
                    eps_iter=eps_iter,
                    nb_iter=nb_iter,
                    norm=np.inf,
                    clip_min=0,
                    clip_max=1,
                    y=[target],
                    targeted=True,
                    sanity_checks=False)

    y_hat_adv = classify(model, noise)
    st.table(y_hat_adv)
    # adv_img = fast_gradient_method(model, align, eps, np.inf)
    # st.info(f"Attack done, {noise.shape} {noise.numpy().max()}")
    
    noise = noise.numpy().squeeze()*0.4
    
    # saved_img = np.uint8(noise.numpy().squeeze())
    # saved_img = Image.fromarray(saved_img)
    # saved_img.save("src/saved_frames/test2.jpg")

    if (np.argmax(y_hat_adv) == 6) and (1 - np.max(y_hat_adv) <= 0.05):
        st.image(adv_img.numpy().squeeze() + noise, channels="RGB", clamp=True)
        st.success("PERSONNE AUTORISEE")
    else:
        st.image(adv_img.numpy().squeeze(), channels="RGB", clamp=True)
        st.error("PERSONNE INCONNUE")


    # st.image(adv_img.numpy().squeeze() + noise, clamp=True, output_format="JPEG")
