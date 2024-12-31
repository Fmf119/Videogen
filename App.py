import streamlit as st
import torch
from diffusers import StableDiffusionPipeline
import moviepy.editor as mp
import os
from PIL import Image

# Load Stable Diffusion model without limitations
@st.cache_resource
def load_model():
    model = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4-original", torch_dtype=torch.float16)
    model = model.to("cuda")  # Ensure the model uses GPU if available, otherwise defaults to CPU
    return model

# Generate an image using the text-to-image model
def generate_image(prompt, model):
    try:
        image = model(prompt).images[0]
        return image
    except Exception as e:
        st.error(f"Error generating image: {e}")
        return None

# Stitch images into a video using MoviePy
def create_video_from_images(image_paths, output_path, fps=24):
    clips = []
    for img_path in image_paths:
        img_clip = mp.ImageClip(img_path).set_duration(1)  # each image is displayed for 1 second
        clips.append(img_clip)
    
    video = mp.concatenate_videoclips(clips, method="compose")
    video.write_videofile(output_path, fps=fps)

# Streamlit UI for the user
st.title("AI Video Generator")

# Prompt input for video creation
prompt = st.text_area("Enter your video description:")
num_frames = st.number_input("Number of frames for the video:", min_value=1, max_value=50, value=10)

if st.button("Generate Video"):
    if prompt.strip():
        st.spinner("Generating images...")

        # Load the model
        model = load_model()

        # Generate images based on the text prompt
        image_paths = []
        for i in range(num_frames):
            # Generate an image
            image = generate_image(prompt, model)
            if image:
                image_path = f"/tmp/{i}_{prompt.replace(' ', '_')}.png"
                image.save(image_path)
                image_paths.append(image_path)

        # Create the video from the generated images
        video_path = "/tmp/generated_video.mp4"
        create_video_from_images(image_paths, video_path)

        # Show the video to the user
        st.success("Video Generated Successfully!")
        st.video(video_path)

        # Allow user to download the video
        with open(video_path, "rb") as video_file:
            st.download_button("Download Video", video_file, file_name="generated_video.mp4", mime="video/mp4")
    else:
        st.warning("Please enter a prompt.")
