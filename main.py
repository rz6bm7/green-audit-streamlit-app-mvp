# main.py - Production-Ready Core Code 
import streamlit as st 
from transformers import pipeline 
import requests 
from io import BytesIO 
 
# Initialize AI models 
#vision_analyzer = pipeline("image-to-text", model="Salesforce/blip2-opt-2.7b") 
#vision_analyzer = pipeline("image-to-text", model="Salesforce/blip2-opt-2.7b", device_map="auto", torch_dtype=torch.float16)
vision_analyzer = pipeline("image-to-text", model="Salesforce/blip2-opt-2.7b-fp16-clip", device_map="auto", torch_dtype=torch.float16)
#text_analyzer = pipeline("sentiment-analysis")
eco_classifier = pipeline("text-classification", model="climatebert/environmental-claims") 
 
def analyze_image(image): 
    """Process user-uploaded image and generate eco-analysis""" 
    try: 
        # Convert image to text 
        text_desc = vision_analyzer(image)[0]['generated_text'] 
 
        # Classify environmental impact 
        eco_score = eco_classifier(text_desc)[0] 
 
        return { 
            'description': text_desc, 
            'eco_score': eco_score['label'], 
            'confidence': eco_score['score'] 
        } 
    except Exception as e: 
        return {"error": f"Analysis failed: {str(e)}"} 
 
def get_affiliate_links(search_term): 
    """Fetch eco-friendly alternatives""" 
    resp = requests.get( 
        f"https://api.affiliate.com/products?search={search_term}&category=eco", 
        headers={"Authorization": "Bearer YOUR_AFFILIATE_KEY"} 
    ) 
    if resp.status_code == 200:  
        try: 
            data = resp.json() 
            if 'results' in data and isinstance(data['results'], list):  
                return data['results'][:3] 
            else: 
                return []  
        except json.JSONDecodeError: 
            return []  
    else: 
        return []  
 
# Streamlit UI 
st.title("🟢 Green Audit AI") 
uploaded_file = st.file_uploader("Upload shopping cart/product screenshot", type=["png", "jpg"]) 
 
if uploaded_file: 
    analysis = analyze_image(uploaded_file.getvalue()) 
 
    if 'error' not in analysis: 
        st.subheader(f"Eco Score: {analysis['eco_score'].upper()} ({analysis['confidence']:.0})") 
        st.caption(f"AI Analysis: {analysis['description']}") 
 
        with st.expander("🛍️ See Sustainable Alternatives"): 
            products = get_affiliate_links(analysis['description']) 
            if products:  
                for prod in products: 
                    st.markdown(f"[{prod['name']}]({prod['affiliate_url']}) - ${prod['price']}") 
                    st.caption(f"Eco Benefits: {prod['eco_features']}") 
            else: 
                st.info("No sustainable alternatives found for this item.")  
 
        st.button("📈 Get Detailed Report", disabled=True) 
    else: 
        st.error(analysis['error']) 
 
st.markdown("---\n*AI analysis powered by ClimateBERT | Affiliate links support our mission*") 
test_text = "This is a test, and I am feeling happy."
sentiment_result = text_analyzer(test_text)
st.write(f"Sentiment analysis test: '{test_text}' - Result: {sentiment_result}")
