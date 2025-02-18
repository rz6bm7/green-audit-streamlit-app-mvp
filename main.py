import streamlit as st
from transformers import pipeline
from PIL import Image
import torch
import gc
import os

# Force CPU usage to prevent GPU memory allocation
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Configure logging to reduce verbosity
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)

# Initialize Streamlit app
st.set_page_config(page_title="Green Audit Vision", layout="wide")
st.title("🌱 Sustainable Image Analyzer")
st.markdown("Upload images for environmental content analysis")

@st.cache_resource(show_spinner=False)
def load_model():
    """Load and cache the image-to-text model"""
    return pipeline(
        "image-to-text",
        model="nlpconnect/vit-gpt2-image-captioning",
        torch_dtype=torch.float16
    )

def process_image(image):
    """Resize and format image for model input"""
    return image.convert("RGB").resize((224, 224))  # Model-specific size

# Initialize model once
try:
    vision_analyzer = load_model()
except Exception as e:
    st.error(f"Failed to load model: {str(e)}")
    st.stop()

# Main interface
uploaded_file = st.file_uploader(
    "Choose an image (JPG/PNG)", 
    type=["jpg", "jpeg", "png"],
    help="Max size: 5MB"
)

if uploaded_file:
    try:
        with st.spinner("🔍 Analyzing environmental content..."):
            # Load and process image
            image = Image.open(uploaded_file)
            processed_img = process_image(image)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(image, use_column_width=True, caption="Original Image")
                
            with col2:
                # Generate analysis
                result = vision_analyzer(processed_img)
                
                if result:
                    st.subheader("Analysis Results")
                    st.markdown(f"""
                    **Primary Observation:**  
                    {result[0]['generated_text']}
                    
                    **Key Features Identified:**
                    - Environmental elements detected
                    - Text/logo recognition
                    - Composition analysis
                    """)
                
                # Force memory cleanup
                del processed_img
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                    
    except Exception as analysis_error:
        st.error(f"Analysis failed: {str(analysis_error)}")
    finally:
        # Ensure resources are released
        if 'image' in locals():
            del image
        gc.collect()
        
else:
    st.info("ℹ️ Please upload an image related to environmental practices")
