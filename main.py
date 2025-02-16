import streamlit as st
from transformers import pipeline
from PIL import Image

vision_analyzer = pipeline("image-to-text")

st.title("Minimal Pipeline Test")
st.write("Upload an image to test the minimal image-to-text pipeline.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("Analyzing image...")
    try:
        result = vision_analyzer(image)
        st.write("AI Output:")
        st.write(result)
    except Exception as e:
        st.error(f"Error during AI analysis: {e}")
