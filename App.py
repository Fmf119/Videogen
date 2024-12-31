import streamlit as st
import cv2
import numpy as np
from diffusers import StableDiffusionPipeline
from PIL import Image
import os

# Initialize Hugging Face Model
@st.cache_resource
def load_model():
    return StableDiffusionPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4",
        torch_dtype="float16",
        use_auth_token=True  # Replace with your Hugging Face token if needed
    ).to("cuda" if torch.cuda.is_available() else "cpu")

# Generate Frames
def generate_frames(prompt, model, num_frames=100):
    frames = []
    for i in range(num_frames):
        try:
            image = model(prompt).images[0]
            frames.append(np.array(image))
        except Exception as e:
            st.error(f"Error generating frame {i+1}: {e}")
            break
    return frames

# Convert Frames to Video
def create_video(frames, output_path, fps=10):
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in frames:
        video.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    video.release()

# Streamlit App
st.title("AI Video Generator with Hugging Face")

auth_token = st.text_input("Enter your Hugging Face Token", type="password")
if auth_token:
    st.success("Token set successfully!")

prompt = st.text_area("Enter a text prompt for your video:")

num_frames = st.slider("Number of frames", 10, 100, 30)
fps = st.slider("Frames per second", 1, 30, 10)

if st.button("Generate Video"):
    if not prompt.strip():
        st.warning("Please enter a valid text prompt.")
    else:
        with st.spinner("Loading model..."):
            model = load_model()

        with st.spinner("Generating frames..."):
            frames = generate_frames(prompt, model, num_frames)

        if frames:
            output_path = "generated_video.mp4"
            with st.spinner("Creating video..."):
                create_video(frames, output_path, fps)
            st.success("Video generated successfully!")
            st.video(output_path)
        else:
            st.error("Video generation failed.")
