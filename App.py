import cv2
import numpy as np
import streamlit as st
import os

# Set up the sidebar for input
st.sidebar.title("AI Video Generator")
task = st.sidebar.radio("Select a task:", ["Generate Video", "Upload and Process Video"])

# Function to handle video generation (placeholder logic here)
def generate_video(prompt):
    try:
        generated_video_path = "/tmp/generated_video.mp4"
        # Placeholder logic: Here, integrate your AI model
        if os.path.exists("sample_input_video.mp4"):
            input_video = cv2.VideoCapture("sample_input_video.mp4")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(generated_video_path, fourcc, 30, (640, 480))
            while input_video.isOpened():
                ret, frame = input_video.read()
                if ret:
                    out.write(frame)
                else:
                    break
            input_video.release()
            out.release()
            return generated_video_path
        else:
            st.error("Sample input video not found.")
            return None
    except Exception as e:
        st.error(f"Error generating video: {e}")
        return None

# User Input and Video Generation
if task == "Generate Video":
    st.subheader("🎬 Generate AI Video:")
    video_prompt = st.text_area("Enter your video description:", "")
    
    if st.button("Generate Video"):
        if video_prompt.strip():
            with st.spinner("Generating video..."):
                video_path = generate_video(video_prompt)
                if video_path:
                    st.success("Video Generated Successfully!")
                    st.video(video_path)
                else:
                    st.error("Video generation failed.")
        else:
            st.warning("Please enter a video description.")

# Upload and Process Existing Video
elif task == "Upload and Process Video":
    st.subheader("📤 Upload and Process Video:")
    uploaded_video = st.file_uploader("Choose a video file...", type=["mp4", "mov", "avi"])
    
    if uploaded_video is not None:
        video_path = os.path.join("/tmp", "uploaded_video.mp4")
        with open(video_path, "wb") as f:
            f.write(uploaded_video.read())
        
        st.success("Video uploaded successfully!")
        st.video(video_path)
        
        # Optional: Allow processing of uploaded video (e.g., trimming, effects)
        process_button = st.button("Process Video")
        if process_button:
            st.spinner("Processing video...")
            try:
                input_video = cv2.VideoCapture(video_path)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter("/tmp/processed_video.mp4", fourcc, 30, (640, 480))
                while input_video.isOpened():
                    ret, frame = input_video.read()
                    if ret:
                        # Just an example: applying a simple effect like flipping the video
                        frame = cv2.flip(frame, 0)
                        out.write(frame)
                    else:
                        break
                input_video.release()
                out.release()
                st.success("Video processed successfully!")
                st.video("/tmp/processed_video.mp4")
            except Exception as e:
                st.error(f"Error processing video: {e}")
