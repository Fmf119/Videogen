import streamlit as st
import cv2
import numpy as np
import os

# Function to generate a custom video using OpenCV
def generate_video(prompt, frame_count=100):
    try:
        # Create a video path
        video_path = "output.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4
        out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))

        # Generate frames based on the prompt
        for i in range(frame_count):
            # Example: Create a frame with text based on the prompt
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            color = tuple(np.random.randint(0, 255, size=3).tolist())  # Random color
            cv2.putText(frame, f"{prompt[:30]} Frame {i+1}", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            out.write(frame)

        out.release()
        return video_path
    except Exception as e:
        st.error(f"Error generating video: {e}")
        return None

# Streamlit App Layout
st.title("Unlimited AI Video Generator")
st.sidebar.title("Options")

# Allow users to input their OpenAI API key
st.sidebar.subheader("Enter OpenAI API Key")
openai_key = st.sidebar.text_input("API Key (Optional)", type="password")

# User Task Selection
task = st.sidebar.radio("Select Task:", ["Generate Custom Video", "Upload and Process Video"])

# Generate Video Task
if task == "Generate Custom Video":
    st.subheader("🎬 Generate a Video Without Limits")
    video_prompt = st.text_area("Enter your video description or theme:")
    frame_count = st.number_input("Number of Frames", min_value=10, max_value=1000, value=100, step=10)

    if st.button("Generate Video"):
        if video_prompt.strip():
            st.info("Generating video...")
            video_path = generate_video(video_prompt, frame_count=frame_count)
            if video_path:
                st.success("Video Generated Successfully!")
                st.video(video_path)
            else:
                st.error("Video generation failed.")
        else:
            st.warning("Please enter a video description.")

# Upload and Process Video Task
elif task == "Upload and Process Video":
    st.subheader("📤 Upload and Edit Your Video")
    uploaded_video = st.file_uploader("Choose a video file...", type=["mp4", "mov", "avi"])
    
    if uploaded_video is not None:
        video_path = os.path.join("/tmp", "uploaded_video.mp4")
        with open(video_path, "wb") as f:
            f.write(uploaded_video.read())
        
        st.success("Video uploaded successfully!")
        st.video(video_path)
        
        # Optional: Allow basic processing of the uploaded video
        if st.button("Process Uploaded Video"):
            try:
                st.spinner("Processing video...")
                cap = cv2.VideoCapture(video_path)
                processed_path = "processed_video.mp4"
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(processed_path, fourcc, 20.0, (640, 480))

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    # Example: Apply grayscale to the video
                    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    color_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
                    out.write(color_frame)

                cap.release()
                out.release()
                st.success("Video processed successfully!")
                st.video(processed_path)
            except Exception as e:
                st.error(f"Error processing video: {e}")
