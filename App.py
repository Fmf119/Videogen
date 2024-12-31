import openai
import streamlit as st
import cv2
import os
import numpy as np
from PIL import Image
from io import BytesIO

# Set OpenAI API key (can also take from user input)
openai.api_key = st.text_input("Enter your OpenAI API Key:")

# Function to generate text using GPT-4
def generate_text(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",  # Or GPT-4 if available
        prompt=prompt,
        max_tokens=150
    )
    return response['choices'][0]['text']

# Function to generate image from text using OpenAI's DALL-E
def generate_image_from_text(text):
    response = openai.Image.create(
        prompt=text,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    img_data = BytesIO(requests.get(image_url).content)
    img = Image.open(img_data)
    return img

# Function to stitch images into a video
def create_video_from_images(image_list, output_file="output_video.mp4"):
    frame_rate = 1  # 1 image per second
    frame_size = (1024, 1024)  # Adjust according to image size
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, frame_size)
    
    for img in image_list:
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR for OpenCV
        out.write(frame)
    
    out.release()
    return output_file

# Streamlit interface
st.title("AI Video Generator")

# Take user input for video script
script_input = st.text_area("Enter a script or description for your video:")

if script_input:
    # Generate text based on user input (or use GPT-4 for more complex prompts)
    generated_text = generate_text(script_input)
    st.write("Generated Script: ", generated_text)
    
    # Generate images based on the generated script
    image_list = []
    for i in range(5):  # Let's say we want to generate 5 images for the video
        image = generate_image_from_text(generated_text)
        image_list.append(image)
    
    # Create the video from images
    video_path = create_video_from_images(image_list)
    st.success("Video generated successfully!")
    
    # Show the video
    st.video(video_path)
