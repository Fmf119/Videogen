import streamlit as st
from moviepy.editor import VideoFileClip
import os

# Set up the sidebar for input
st.sidebar.title("AI Video Generator")
task = st.sidebar.radio("Select a task:", ["Generate Video", "Upload and Process Video"])

# Function to handle video generation (this is a placeholder; integrate your AI model here)
def generate_video(prompt):
    try:
        generated_video_path = "/tmp/generated_video.mp4"
        # Placeholder logic: Here, integrate your video generation AI model
        if os.path.exists("sample_input_video.mp4"):
            clip = VideoFileClip("sample_input_video.mp4").subclip(0, 10)
            clip.write_videofile(generated_video_path)
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
                video_path = generate_video(video_prompt)  # Integrate with your AI model
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
                video_clip = VideoFileClip(video_path)
                processed_clip = video_clip.subclip(0, 5)  # Just an example of video manipulation
                processed_clip.write_videofile("/tmp/processed_video.mp4")
                st.success("Video processed successfully!")
                st.video("/tmp/processed_video.mp4")
            except Exception as e:
                st.error(f"Error processing video: {e}")
