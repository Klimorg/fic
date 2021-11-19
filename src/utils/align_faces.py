import numpy as np
import tensorflow as tf
from mtcnn.mtcnn import MTCNN
from PIL import Image

detector = MTCNN()


def extract_face(filename, required_size=(224, 224)):
    # load image from file
    image = Image.open(filename)
    # convert to RGB, if needed
    image = image.convert("RGB")
    # convert to array
    pixels = np.asarray(image)
    # detect faces in the image
    results = detector.detect_faces(pixels)
    # extract the bounding box from the first face
    x1, y1, width, height = results[0]["box"]
    # bug fix
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    # extract the face
    face = pixels[y1:y2, x1:x2]
    # resize pixels to the model size
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = np.asarray(image)

    return face_array
