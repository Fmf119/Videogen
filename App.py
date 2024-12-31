import streamlit as st
import torch
from diffusers import StableDiffusionPipeline
import moviepy.editor as mp
import os
from PIL import Image

# Load Stable Diffusion model
@st.cache_resource
def load_model():
    model = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4-original", torch_dtype=torch.float16)
    model = model.to("cuda")
    return model

# Function to generate an image from the text prompt
def generate_image(prompt, model):
    image = model(prompt).images[0]
    return image

# Function to create video from a series of images
def create_video_from_images(image_paths, output_path, fps=24):
    clips = []
    for img_path in image_paths:
        img_clip = mp.ImageClip(img_path).set_duration(1)  # each frame lasts 1 second
        clips.append(img_clip)
    video = mp.concatenate_videoclips(clips, method="compose")
    video.write_videofile(output_path, fps=fps)

# Streamlit interface
st.title("AI Video Generator from Text")

# Get user input for text prompt
prompt = st.text_area("Enter your text description:")
num_frames = st.number_input("Number of frames for the video:", min_value=1, max_value=50, value=10)

if st.button("Generate Video"):
    if prompt.strip():
        st.spinner("Generating images...")

        # Load the model
        model = load_model()

        # Generate images for video
        image_paths = []
        for i in range(num_frames):
            # Generate each image
            image = generate_image(prompt, model)
            image_path = f"/tmp/{i}_{prompt.replace(' ', '_')}.png"
            image.save(image_path)
            image_paths.append(image_path)

        # Create a video from the generated images
        video_path = "/tmp/generated_video.mp4"
        create_video_from_images(image_paths, video_path)

        # Display the video
        st.success("Video Generated Successfully!")
        st.video(video_path)

        # Optionally, allow the user to download the video
        with open(video_path, "rb") as video_file:
            st.download_button("Download Video", video_file, file_name="generated_video.mp4", mime="video/mp4")
