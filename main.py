import streamlit as st
from transformers import pipeline

vision_analyzer = pipeline("image-to-text")

st.title("Minimal Pipeline Test")
st.write("This minimal pipeline call is being used for diagnostic purposes.")
