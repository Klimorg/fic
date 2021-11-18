import threading
from typing import Union

import av
import numpy as np
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

# webrtc_streamer(key="example")


def main():
    class VideoTransformer(VideoTransformerBase):
        # frame_lock: threading.Lock  # `transform()` is running in another thread, then a lock object is used here for thread-safety.
        in_image: Union[np.ndarray, None]
        # out_image: Union[np.ndarray, None]

        def __init__(self) -> None:
            self.frame_lock = threading.Lock()
            self.in_image = None
            self.out_image = None

        def recv(self, frame: av.VideoFrame) -> np.ndarray:
            in_image = frame.to_ndarray(format="bgr24")

            with self.frame_lock:
                self.in_image = in_image

            return av.VideoFrame.from_ndarray(in_image, format="bgr24")

    ctx = webrtc_streamer(
        key="snapshot", video_processor_factory=VideoTransformer
    )

    if ctx.video_transformer:
        if st.button("Snapshot"):
            with ctx.video_transformer.frame_lock:
                in_image = ctx.video_transformer.in_image

            if in_image is not None:
                st.write("Input image:")
                st.image(in_image, channels="BGR")

            else:
                st.warning("No frames available yet.")


main()
