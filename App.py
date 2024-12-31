import streamlit as st
import openai
import cv2
import numpy as np
import os
from pathlib import Path

# Function to create frames using OpenAI (DALL-E) API
def generate_frame(prompt, frame_number):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response["data"][0]["url"]
        frame = cv2.imdecode(
            np.asarray(bytearray(st.file_uploader(image_url).read()), dtype=np.uint8),
            cv2.IMREAD_COLOR
        )
        return frame
    except Exception as e:
        st.error(f"Error generating frame {frame_number}: {e}")
        return None

# Function to stitch frames into a video
def create_video_from_frames(frames, output_path, fps=10):
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in frames:
        video.write(frame)
    video.release()

# Streamlit App Layout
st.title("AI Video Generator with OpenAI")
st.sidebar.title("Options")

# Allow users to input their OpenAI API key
st.sidebar.subheader("Enter OpenAI API Key")
openai_key = st.sidebar.text_input("API Key", type="password")

if openai_key:
    openai.api_key = openai_key

    # User Task: Generate a video
    st.subheader("🎬 Generate a Video")
    video_prompt = st.text_area("Enter your video description or theme:")
    num_frames = st.number_input("Number of Frames", min_value=10, max_value=100, value=10, step=1)
    fps = st.number_input("Frames per Second (FPS)", min_value=5, max_value=60, value=10, step=1)

    if st.button("Generate Video"):
        if video_prompt.strip():
            st.info("Generating video frames...")
            frames = []
            for i in range(num_frames):
                frame = generate_frame(f"{video_prompt} frame {i+1}", i+1)
                if frame is not None:
                    frames.append(frame)
            
            if frames:
                st.info("Stitching frames into video...")
                video_path = "output_video.mp4"
                create_video_from_frames(frames, video_path, fps)
                st.success("Video Generated Successfully!")
                st.video(video_path)
            else:
                st.error("No frames were generated.")
        else:
            st.warning("Please enter a video description.")
else:
    st.warning("Please enter your OpenAI API key to use this feature.")
