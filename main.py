import streamlit as st
from transformers import pipeline
from PIL import Image
import torch
import torchvision.transforms as transforms
import gc

st.title("Green Audit Streamlit App MVP")
st.write("Upload an image for analysis")

@st.cache_resource
def load_model():
    return pipeline("image-to-text", 
                   model="nlpconnect/vit-gpt2-image-captioning",
                   torch_dtype=torch.float16)

vision_analyzer = load_model()

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, use_column_width=True)
    
    with st.spinner("Analyzing..."):
        try:
            analysis = vision_analyzer(image)
            st.write("**Result:**", analysis[0]['generated_text'])
            
            # Force memory cleanup
            gc.collect()
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
