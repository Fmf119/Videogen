import streamlit as st
from huggingface_hub import login
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import cv2
import os

# Set up the sidebar for input
st.sidebar.title("AI Video Generator")
task = st.sidebar.radio("Select a task:", ["Generate Video", "Upload and Process Video"])

# Allow user to enter their Hugging Face API token
huggingface_token = st.sidebar.text_input("Enter your Hugging Face API Token (if using Hugging Face models):", type="password")

# Function to log in to Hugging Face with the token
def login_to_huggingface(token):
    try:
        if token:
            login(token)
            st.success("Successfully logged into Hugging Face!")
        else:
            st.warning("Please enter your Hugging Face token.")
    except Exception as e:
        st.error(f"Failed to log in to Hugging Face: {e}")

# If Hugging Face token is provided, authenticate
if huggingface_token:
    login_to_huggingface(huggingface_token)

# Function to generate image from text using Stable Diffusion
def generate_image_from_prompt(prompt):
    model_id = "CompVis/stable-diffusion-v1-4"
    
    if huggingface_token:
        pipe = StableDiffusionPipeline.from_pretrained(model_id, use_auth_token=huggingface_token, torch_dtype=torch.float16)
        pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

        try:
            # Generate the image
            image = pipe(prompt).images[0]
            output_path = "/tmp/generated_image.png"
            image.save(output_path)
            return output_path
        except Exception as e:
            st.error(f"Error generating image: {e}")
            return None
    else:
        st.warning("Hugging Face token is required to generate the image.")
        return None

# Function to create video from generated images
def create_video_from_images(image_paths, output_path="output_video.mp4", fps=10):
    if not image_paths:
        st.error("No images to generate video.")
        return
    
    frame = cv2.imread(image_paths[0])
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for image_path in image_paths:
        frame = cv2.imread(image_path)
        video.write(frame)

    video.release()
    st.success(f"Video generated successfully: {output_path}")
    return output_path

# User Input and Video Generation
if task == "Generate Video":
    st.subheader("🎬 Generate AI Video:")
    video_prompt = st.text_area("Enter your video description:", "")
    num_frames = st.slider("Select the number of frames", 1, 100, 10)  # Let user select number of frames
    
    if st.button("Generate Video"):
        if video_prompt.strip():
            with st.spinner("Generating video..."):
                # Generate images for each frame
                image_paths = []
                for i in range(num_frames):
                    image_path = generate_image_from_prompt(f"{video_prompt} - frame {i+1}")
                    if image_path:
                        image_paths.append(image_path)

                # Create video from the generated images
                if image_paths:
                    video_path = create_video_from_images(image_paths)
                    st.video(video_path)
                else:
                    st.error("Failed to generate video.")
        else:
            st.warning("Please enter a video description.")
