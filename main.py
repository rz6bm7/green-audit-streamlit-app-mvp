import streamlit as st
from transformers import pipeline
from PIL import Image
import torch
import gc

@st.cache_resource  # Add model caching
def load_model():
    return pipeline("image-to-text", 
                  model="nlpconnect/vit-gpt2-image-captioning",
                  torch_dtype=torch.float16)

vision_analyzer = load_model()

# ... rest of your code ...

# Remove padding=True from this line:
analysis = vision_analyzer(image)  #  No padding parameter
