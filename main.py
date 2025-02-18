import streamlit as st
from transformers import pipeline
from PIL import Image
import torchvision.transforms as transforms  # ADD THIS LINE
import streamlit as st
from transformers import pipeline
from PIL import Image
# Set up the Streamlit app title and instructions
st.title("Green Audit Streamlit App MVP")
st.write("Upload an image to analyze and generate a descriptive output using our vision model.")

# Initialize the image-to-text pipeline from transformers
vision_analyzer = pipeline("image-to-text", padding=True)
# Define image transformations using torchvision.transforms.Compose
image_transform = transforms.Compose([
    transforms.Resize((256, 256)),  # Resize image to 256x256 pixels (adjust size if needed)
    transforms.ToTensor()           # Convert PIL Image to PyTorch tensor
])
# File uploader widget: accepts jpg, jpeg, and png files
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    st.write("Analyzing image...")
    try:
        # Get the output from the image-to-text pipeline
        analysis = vision_analyzer(image)
        st.write("**Analysis Result:**")
        st.write(analysis)
    except Exception as e:
        st.error(f"An error occurred during analysis: {e}")
else:
    st.info("Please upload an image file to get started.")
