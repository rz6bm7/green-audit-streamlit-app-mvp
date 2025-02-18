import streamlit as st
from transformers import pipeline
from PIL import Image
import torch
import gc
import os
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="huggingface_hub.file_download")

# Force CPU usage and disable unnecessary logs
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Configure logging
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)

st.set_page_config(page_title="Green Audit Vision", layout="wide")
st.title("🌱 Sustainable Image Analyzer")
st.markdown("Upload images for environmental content analysis")

@st.cache_resource(show_spinner=False)
def load_model():
    return pipeline(
        "image-to-text",
        model="nlpconnect/vit-gpt2-image-captioning",
        torch_dtype=torch.float16
    )

try:
    vision_analyzer = load_model()
except Exception as e:
    st.error(f"Model loading failed: {str(e)}")
    st.stop()

def process_image(image):
    return image.convert("RGB").resize((224, 224))

uploaded_file = st.file_uploader(
    "Choose an image (JPG/PNG)", 
    type=["jpg", "jpeg", "png"],
    help="Max size: 5MB"
)

if uploaded_file:
    try:
        with st.spinner("Analyzing..."):
            image = Image.open(uploaded_file)
            processed_img = process_image(image)
            
            col1, col2 = st.columns(2)
            with col1:
                st.image(image, use_column_width=True)
                
            with col2:
                result = vision_analyzer(processed_img)
                if result:
                    st.subheader("Analysis Results")
                    st.write(result[0]['generated_text'])
                
                # Memory cleanup
                del processed_img
                gc.collect()
                
    except Exception as e:
        st.error(f"Error: {str(e)}")
    finally:
        if 'image' in locals():
            del image
        gc.collect()
else:
    st.info("Please upload an image file")
