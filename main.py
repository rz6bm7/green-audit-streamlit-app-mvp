import streamlit as st
from transformers import pipeline
from PIL import Image
import torch
import gc
import os
import logging

# Force CPU and full precision
os.environ["CUDA_VISIBLE_DEVICES"] = ""
torch.set_default_dtype(torch.float32)  # Critical fix

# Configure logging
logging.getLogger("transformers").setLevel(logging.ERROR)

# App setup
st.set_page_config(page_title="Green Audit", layout="centered")
st.title("🌿 Environmental Image Analysis")

@st.cache_resource(show_spinner=False)
def load_model():
    return pipeline(
        "image-to-text",
        model="nlpconnect/vit-gpt2-image-captioning",
        device=-1  # Force CPU
    )

try:
    analyzer = load_model()
except Exception as e:
    st.error(f"Model failed to load: {str(e)}")
    st.stop()

def process_image(upload):
    return Image.open(upload).convert("RGB").resize((224, 224))

upload = st.file_uploader("Upload eco-related image", type=["jpg", "jpeg", "png"])

if upload:
    try:
        with st.spinner("Analyzing..."):
            img = process_image(upload)
            result = analyzer(img)[0]['generated_text']
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(img, use_column_width=True)
            with col2:
                st.subheader("Analysis Results")
                st.write(result)
                
            # Memory cleanup
            del img
            gc.collect()
            
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
    finally:
        if 'img' in locals():
            del img
        gc.collect()
else:
    st.info("Please upload an image to begin")
