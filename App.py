import streamlit as st
import cv2
import os

# Set up the sidebar for input
st.sidebar.title("AI Video Generator")
task = st.sidebar.radio("Select a task:", ["Generate Video", "Upload and Process Video"])

# Function to handle video generation (this is a placeholder; integrate your AI model here)
def generate_video(uploaded_video_path):
    try:
        generated_video_path = "/tmp/generated_video.mp4"
        if os.path.exists(uploaded_video_path):
            input_video = cv2.VideoCapture(uploaded_video_path)
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
            st.error(f"Input video not found: {uploaded_video_path}")
            return None
    except Exception as e:
        st.error(f"Error generating video: {e}")
        return None

# User Input and Video Generation
if task == "Generate Video":
    st.subheader("🎬 Generate AI Video:")
    uploaded_video = st.file_uploader("Upload your input video (MP4 format):", type=["mp4", "mov", "avi"])

    if uploaded_video is not None:
        with open("/tmp/uploaded_video.mp4", "wb") as f:
            f.write(uploaded_video.read())

        st.success("Input video uploaded successfully!")
        st.video("/tmp/uploaded_video.mp4")

        if st.button("Generate Video"):
            with st.spinner("Generating video..."):
                video_path = generate_video("/tmp/uploaded_video.mp4")  # Using uploaded video for generation
                if video_path:
                    st.success("Video Generated Successfully!")
                    st.video(video_path)
                else:
                    st.error("Video generation failed.")

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
                video_clip = cv2.VideoCapture(video_path)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter("/tmp/processed_video.mp4", fourcc, 30, (640, 480))
                while video_clip.isOpened():
                    ret, frame = video_clip.read()
                    if ret:
                        # Just an example: applying a simple effect like flipping the video
                        frame = cv2.flip(frame, 0)
                        out.write(frame)
                    else:
                        break
                video_clip.release()
                out.release()
                st.success("Video processed successfully!")
                st.video("/tmp/processed_video.mp4")
            except Exception as e:
                st.error(f"Error processing video: {e}")
