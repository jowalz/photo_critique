import streamlit as st
from PIL import Image
import google.generativeai as genai  # Google Generative AI Python SDK that contains methods and classes to interact with Google's generative AI models.

# ---------------------------------------------------
# 1. Initialize Environment (No direct action needed for Streamlit Secrets)
# ---------------------------------------------------

# ---------------------------------------------------
# 2. Configure API Key using Streamlit Secrets
# ---------------------------------------------------
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

def get_gemini_response(input_prompt, image, language):
    """
    Sends the input prompt, image data, and selected language to Gemini and retrieves the response.
    
    Args:
        input_prompt (str): The prompt instructing the AI on how to critique the photo.
        image (list): A list containing image data prepared for the API call.
        language (str): The selected language for the critique.
    
    Returns:
        str: The text response generated by the AI model.
    """
    # Modify the prompt to include the selected language
    localized_prompt = f"Language: {language}\n\n{input_prompt}"
    response = model.generate_content([localized_prompt, image[0]])
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
st.set_page_config(page_title="Photo Critique App", layout="centered")

# Display App Title
st.title("Photo Critique App")

# Set Up Language Selector
st.write("Select your preferred language:")
supported_languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de"
}
selected_language = st.selectbox("Language", options=supported_languages.keys(), index=0)
language_code = supported_languages[selected_language]

# Set Up Image Upload Interface
uploaded_file = st.file_uploader("Upload Your Photo to Receive AI-Powered Critique", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Photo", use_container_width=True)

# ---------------------------------------------------
# 5. User Interaction & Generate Critique
# ---------------------------------------------------

# Submit Button to Generate Critique
if st.button("Submit"):
    try:
        # Handle Image Upload and Display
        image_data = get_image_content(uploaded_file)

        # Define Critique Prompt
        input_prompt = """
        Provide a constructive and detailed photographic critique, offering specific feedback and suggestions for improvement on the following aspects:\n\n
        - Composition: Analyze ...\n
        - Lighting: Evaluate ...\n
        - Focus and Sharpness: Assess ...\n
        - Exposure: Determine ...\n
        - Color Balance: Examine ...\n
        - Creativity and Impact: Consider ...\n\n
        Begin your critique with a positive two-sentence summary ...\n\n
        Structure your detailed feedback into two distinct sections:\n\n
        **Positive Critique:** ...\n\n
        **Recommended Optimizations:** ...\n\n
        Conclude your critique with an overall rating of the photo on a scale of 1 to 10, where 10 represents the highest possible score.
        """

        # Generate Critique
        response = get_gemini_response(input_prompt, image_data, language_code)

        # Display AI-Generated Critique
        st.subheader("Photo Critique")
        st.write(response)
    except FileNotFoundError as e:
        # Manage Errors: File Not Uploaded
        st.error(str(e))
    except Exception as e:
        # Manage Errors: Other Exceptions
        st.error(f"An error occurred: {e}")
