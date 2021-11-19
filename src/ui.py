import numpy as np
import streamlit as st

from utils.align_faces import extract_face
from utils.face_recognition import classify
from utils.video_capture import capture

st.header("Démonstrateur Attaque antagoniste CITC !")


capture()

if st.sidebar.button("Lancer la reconnaissace faciale"):
    align = extract_face("src/saved_frames/test.jpg")
    st.info("Visage detecté !")
    y_hat = classify(align)

    if (np.argmax(y_hat) == 6) and (1 - np.max(y_hat) <= 0.05):
        st.image(align, channels="RGB")
        st.success("PERSONNE AUTORISEE")
    else:
        st.image(align, channels="RGB")
        st.error("PERSONNE INCONNUE")
