import streamlit as st
import os
from PIL import Image
import requests
import cv2

# Function to generate an image from text (use your preferred model/API)
def generate_image_from_text(prompt):
    # Here we use OpenAI’s DALL·E API, or you can use any model that can generate images from text.
    # You can replace this with any other API or model
    # (this is just an example, you'll need an API key for OpenAI or a similar service).
    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers={"Authorization": "Bearer YOUR_OPENAI_API_KEY"},
        json={
            "prompt": prompt,
            "n": 1,
            "size": "512x512"
        }
    )
    response_json = response.json()
    image_url = response_json["data"][0]["url"]
    
    # Download the image
    img_data = requests.get(image_url).content
    img_path = "/tmp/generated_image.png"
    with open(img_path, "wb") as img_file:
        img_file.write(img_data)
    
    return img_path

# Function to generate a video from images
def generate_video_from_images(image_paths, output_path, frame_rate=1):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, frame_rate, (512, 512))

    for image_path in image_paths:
        image = cv2.imread(image_path)
        video_writer.write(image)

    video_writer.release()

# Set up the sidebar for input
st.sidebar.title("AI Video Generator")
task = st.sidebar.radio("Select a task:", ["Generate Video from Text"])

if task == "Generate Video from Text":
    st.subheader("🎬 Generate AI Video from Text:")
    video_prompt = st.text_area("Enter your video description:", "")

    if st.button("Generate Video"):
        if video_prompt.strip():
            with st.spinner("Generating video..."):
                # Generate images based on the text prompt
                image_paths = []
                for _ in range(5):  # Generate 5 images based on text prompt
                    img_path = generate_image_from_text(video_prompt)
                    image_paths.append(img_path)

                # Create a video from the images
                video_path = "/tmp/generated_video.mp4"
                generate_video_from_images(image_paths, video_path)

                # Display the video
                st.success("Video Generated Successfully!")
                st.video(video_path)
        else:
            st.warning("Please enter a video description.")
