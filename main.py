import streamlit as st
from transformers import pipeline

# Initialize AI models - ONLY this part for now
#vision_analyzer = pipeline("image-to-text", model="google/pix2struct-textcaps-base", device_map="auto", torch_dtype=torch.float16)
#vision_analyzer = pipeline("image-to-text", model="google/pix2struct-textcaps-base", device_map="auto")
vision_analyzer = pipeline("image-to-text")
# NO Streamlit UI code or image processing code for now
# Just the imports and pipeline initialization
