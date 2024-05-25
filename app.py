from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def get_gemini_repsonse(input_prompt,image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Nutrify")

st.header("Nutrify")
st.write("Upload your food picture and get detailed nutritional information.")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Analyze the Picture")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories, protein
               2. Item 2 - no of calories, protein
               ----
               ----
        Also mention disease risk from these items
        Finally you can also mention whether the food items are healthy or not and Suggest Some Healthy Alternative 
               is below format          
               1. Item 1 - no of calories, protein
               2. Item 2 - no of calories, protein
               ----
               ----
"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data)
    st.subheader("The Response is")
    st.write(response)
st.warning("Nutrify can make mistakes.")
