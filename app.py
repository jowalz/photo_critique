import streamlit as st
from PIL import Image
import google.generativeai as genai  # Google Generative AI Python SDK that contains methods and classes to interact with Google's generative AI models.

# ---------------------------------------------------
# 1. Initialize Environment (No direct action needed for Streamlit Secrets)
# ---------------------------------------------------

# Quick Note on Inspiration:
# Inspired by the need to provide users with expert photo critiques using advanced AI models,
# enhancing photography skills through constructive feedback.

# ---------------------------------------------------
# 2. Configure API Key using Streamlit Secrets
# ---------------------------------------------------

# Access the API key from Streamlit secrets
try:
    api_key = st.secrets["API_KEY"]
    if not api_key:
        st.error("Google API key not found in Streamlit Secrets! Please add it to the Secrets section of your app.")
        st.stop()
    # Configure Google Generative AI SDK with the API key
    genai.configure(api_key=api_key)
except KeyError:
    st.error("Google API key not found in Streamlit Secrets! Please add a secret named 'API_KEY' with your key.")
    st.stop()

# ---------------------------------------------------
# 3. Initialize Generative Model & Define Functions
# ---------------------------------------------------

# Initialize the Generative Model
model = genai.GenerativeModel("gemini-1.5-flash-8b")  # Initializes an instance of the GenerativeModel class from the genai SDK

def get_gemini_response(input_prompt, image):
    """
    Sends the input prompt and image data to Gemini and retrieves the response.
    
    Args:
        input_prompt (str): The prompt instructing the AI on how to critique the photo.
        image (list): A list containing image data prepared for the API call.
    
    Returns:
        str: The text response generated by the AI model.
    """
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def get_image_content(uploaded_file):
    """
    Processes the uploaded image file and prepares it for the API call.
    
    Args:
        uploaded_file (UploadedFile): The image file uploaded by the user.
    
    Returns:
        list: A list of dictionaries containing MIME type and image data.
    
    Raises:
        FileNotFoundError: If no file is uploaded.
    """
    if uploaded_file is not None:
        image_byte_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": image_byte_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("File not uploaded")

# ---------------------------------------------------
# 4. Streamlit Interface Setup
# ---------------------------------------------------

# Configure Streamlit Page
st.set_page_config(page_title="", layout="centered")

# Display App Title
# st.markdown("<h1 style='text-align: center;'>PhotoCritique App</h1>", unsafe_allow_html=True)

# Optional: Additional Inputs (Scene Type, Desired Feedback, etc.)
# For simplicity, we'll keep only the image upload in this example.

# Set Up Image Upload Interface
uploaded_file = st.file_uploader("Upload your Photo for Critique", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Uploaded Photo", use_container_width=True)

# ---------------------------------------------------
# 5. User Interaction & Generate Critique
# ---------------------------------------------------

# Submit Button to Generate Critique
submit = st.button("Press Button Get Critique")

# Define Critique Prompt
input_prompt = """
You are an expert professional photographer. Please critique the uploaded photo focusing on the following aspects:
- Composition
- Lighting
- Focus and Sharpness
- Exposure
- Color Balance
- Creativity and Impact

Provide constructive feedback and suggestions for improvement in a clear and detailed manner.
Atructure your answers in 2 sections: Positive Critique and Recommended Optimizations. Keep your answers 1 sentence per aspect long, and use an upbeat, chipper tone

"""

if submit:
    try:
        # Handle Image Upload and Display
        image_data = get_image_content(uploaded_file)
        
        # Generate Critique
        response = get_gemini_response(input_prompt, image_data)
        
        # Display AI-Generated Critique
        st.subheader("Photo Critique")
        st.write(response)
    except FileNotFoundError as e:
        # Manage Errors: File Not Uploaded
        st.error(str(e))
    except Exception as e:
        # Manage Errors: Other Exceptions
        st.error(f"An error occurred: {e}")
