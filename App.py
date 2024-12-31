import streamlit as st
import openai
import cv2
import numpy as np
import requests
from pathlib import Path

# Function to download image from URL
def download_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        return cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    else:
        raise Exception(f"Failed to download image: {response.status_code}")

# Function to create a single frame
def generate_frame(prompt, frame_number):
    try:
        response = openai.Image.create(
            prompt=f"{prompt} - frame {frame_number}",
            n=1,
            size="512x512"
        )
        image_url = response["data"][0]["url"]
        frame = download_image(image_url)
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

    # User Input for Video Generation
    st.subheader("🎬 Generate a Video")
    video_prompt = st.text_area("Enter your video description or theme:")
    total_frames = st.number_input("Total Number of Frames", min_value=10, max_value=10000, value=200, step=10)
    batch_size = st.number_input("Batch Size (frames per batch)", min_value=10, max_value=100, value=50, step=10)
    fps = st.number_input("Frames per Second (FPS)", min_value=5, max_value=60, value=10, step=1)

    if st.button("Generate Video"):
        if video_prompt.strip():
            st.info("Generating video frames in batches...")
            frames = []
            num_batches = total_frames // batch_size + (1 if total_frames % batch_size else 0)
            for batch in range(num_batches):
                st.info(f"Generating batch {batch + 1} of {num_batches}...")
                for i in range(batch * batch_size, min((batch + 1) * batch_size, total_frames)):
                    frame = generate_frame(video_prompt, i + 1)
                    if frame is not None:
                        frames.append(frame)
                
                # Save intermediate frames to free memory
                temp_video_path = f"temp_batch_{batch + 1}.mp4"
                if frames:
                    st.info(f"Stitching batch {batch + 1} into a temporary video...")
                    create_video_from_frames(frames, temp_video_path, fps)
                    st.video(temp_video_path)
                frames.clear()  # Clear frames to free memory

            # Combine temporary videos into a final video
            st.info("Combining all batches into the final video...")
            final_video_path = "output_video.mp4"
            os.system(f"ffmpeg -f concat -safe 0 -i <(for f in temp_batch_*.mp4; do echo file $f; done) -c copy {final_video_path}")
            st.success("Video Generated Successfully!")
            st.video(final_video_path)
        else:
            st.warning("Please enter a video description.")
else:
    st.warning("Please enter your OpenAI API key to use this feature.")
