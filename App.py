import streamlit as st
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import os
import subprocess
import openai

# Load Stable Diffusion model
@st.cache_resource
def load_model():
    model = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4-original", torch_dtype=torch.float16)
    model = model.to("cuda")  # Ensure GPU usage if available
    return model

# Generate an image from a text prompt using OpenAI API key if provided
def generate_image(prompt, model, openai_api_key):
    try:
        # Authenticate with OpenAI API if key is provided
        if openai_api_key:
            openai.api_key = openai_api_key
        else:
            st.error("OpenAI API key is required for text generation.")
            return None

        # Use the Stable Diffusion model to generate the image
        image = model(prompt).images[0]
        return image
    except Exception as e:
        st.error(f"Error generating image: {e}")
        return None

# Function to create video from images using FFMPEG
def create_video_from_images(image_paths, output_path, fps=24):
    # Create an input file list for FFMPEG
    input_file_list = "/tmp/images.txt"
    with open(input_file_list, "w") as f:
        for image_path in image_paths:
            f.write(f"file '{image_path}'\n")
    
    # Run the FFMPEG command to create a video from the images
    command = [
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", input_file_list, 
        "-vsync", "vfr", "-pix_fmt", "yuv420p", output_path
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        st.error(f"Error creating video: {e}")

# Streamlit UI for the user
st.title("AI Video Generator")

# User input for the OpenAI API key
openai_api_key = st.text_input("Enter your OpenAI API Key (if needed):")

# User input for the video generation
prompt = st.text_area("Enter your video description:")
num_frames = st.number_input("Number of frames for the video:", min_value=1, max_value=50, value=10)

if st.button("Generate Video"):
    if prompt.strip():
        st.spinner("Generating images...")

        # Load the model
        model = load_model()

        # Generate images based on the prompt
        image_paths = []
        for i in range(num_frames):
            image = generate_image(prompt, model, openai_api_key)
            if image:
                image_path = f"/tmp/{i}_{prompt.replace(' ', '_')}.png"
                image.save(image_path)
                image_paths.append(image_path)

        # Create video from images using FFMPEG
        video_path = "/tmp/generated_video.mp4"
        create_video_from_images(image_paths, video_path)

        # Show the generated video
        st.success("Video Generated Successfully!")
        st.video(video_path)

        # Allow users to download the video
        with open(video_path, "rb") as video_file:
            st.download_button("Download Video", video_file, file_name="generated_video.mp4", mime="video/mp4")
    else:
        st.warning("Please enter a prompt.")
