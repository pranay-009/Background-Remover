import streamlit as st
from PIL import Image
import os

import sys
print(sys.executable)
from src.remover import BackgroundRemover

st.set_page_config(
    page_title="Background Remover",
    page_icon="👋",
)

if __name__ == "__main__":

    obj = BackgroundRemover()

    st.title("DEMO")
    st.write("Upload an image")

    uploaded_file = st.file_uploader("Choose a file",type=["jpg", "png", "jpeg"])
    IMAGE_DIR = "./output"

    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()

        IMAGE_PATH = os.path.join(IMAGE_DIR,uploaded_file.name)
        OUT_PATH =  os.path.join(IMAGE_DIR,"results.png")
        BACKGROUND_PATH = os.path.join(os.getcwd(),"static/background/2.png")
        with open(IMAGE_PATH,"wb") as f:
            f.write(uploaded_file.getbuffer())

        col1, col2 = st.columns(2)
        with col1:
            st.image(IMAGE_PATH, caption="Original Image",use_column_width=True)

        result = obj.process(IMAGE_PATH,BACKGROUND_PATH,OUT_PATH,True)
        with col2:
            image=Image.open(OUT_PATH)
            st.image(result, caption="Result", use_column_width=True)
        