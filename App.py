import streamlit as st
import requests
import tempfile
import cv2
import os

# Function to generate image from text using OpenAI API
def generate_image_from_text(api_key, prompt):
    try:
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"prompt": prompt, "n": 1, "size": "512x512"}
        )
        response.raise_for_status()  # Check for request errors
        response_json = response.json()
        image_url = response_json.get("data", [])[0].get("url", None)
        
        if image_url:
            img_data = requests.get(image_url).content
            img_path = tempfile.mktemp(suffix=".png")
            with open(img_path, "wb") as img_file:
                img_file.write(img_data)
            return img_path
        else:
            st.error("No image URL found in the response.")
            return None
    except Exception as e:
        st.error(f"Error generating image: {e}")
        return None

# Function to generate a video from the images
def generate_video_from_images(image_paths, output_path, frame_rate=1):
    try:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 video
        video_writer = cv2.VideoWriter(output_path, fourcc, frame_rate, (512, 512))

        for image_path in image_paths:
            image = cv2.imread(image_path)
            if image is None:
                st.error(f"Error reading image: {image_path}")
                return None
            video_writer.write(image)

        video_writer.release()
        return output_path
    except Exception as e:
        st.error(f"Error creating video: {e}")
        return None

# Streamlit UI to enter text
st.sidebar.title("AI Video Generator")

# Ask user for the OpenAI API Key
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

task = st.sidebar.radio("Select a task:", ["Generate Video from Text"])

if api_key:
    if task == "Generate Video from Text":
        st.subheader("🎬 Generate AI Video from Text:")
        video_prompt = st.text_area("Enter your video description:", "")

        if st.button("Generate Video"):
            if video_prompt.strip():
                with st.spinner("Generating video..."):
                    # Generate 5 images for the video (you can increase the count for longer videos)
                    image_paths = []
                    for i in range(5):  # You can generate more images here
                        img_path = generate_image_from_text(api_key, video_prompt)
                        if img_path:
                            image_paths.append(img_path)

                    if image_paths:
                        # Create a video from the images
                        video_path = tempfile.mktemp(suffix=".mp4")
                        video_path = generate_video_from_images(image_paths, video_path)

                        if video_path:
                            st.success("Video Generated Successfully!")
                            st.video(video_path)
                        else:
                            st.error("Failed to generate video.")
                    else:
                        st.error("No images were generated.")
            else:
                st.warning("Please enter a video description.")
else:
    st.warning("Please enter your OpenAI API key.")
