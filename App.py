import streamlit as st
import requests
import os
import cv2
import tempfile

# Function to validate OpenAI API Key
def validate_openai_key(api_key):
    try:
        # Test API call to validate the API key
        response = requests.post(
            "https://api.openai.com/v1/models",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        if response.status_code == 200:
            return True
        else:
            st.error(f"Error with the provided API key: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error validating API key: {e}")
        return False

# Function to generate images from text
def generate_image_from_text(api_key, prompt):
    try:
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"prompt": prompt, "n": 1, "size": "512x512"}
        )
        if response.status_code == 200:
            response_json = response.json()
            image_url = response_json.get("data", [])[0].get("url", None)
            if image_url:
                img_data = requests.get(image_url).content
                img_path = tempfile.mktemp(suffix=".png")
                with open(img_path, "wb") as img_file:
                    img_file.write(img_data)
                return img_path
            else:
                st.error("Image URL not found in response.")
                return None
        else:
            st.error(f"Error: Received unexpected status code {response.status_code} from API.")
            return None
    except Exception as e:
        st.error(f"Error generating image: {e}")
        return None

# Function to generate video from images using OpenCV
def generate_video_from_images(image_paths, output_path, frame_rate=1):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 video
    video_writer = cv2.VideoWriter(output_path, fourcc, frame_rate, (512, 512))

    for image_path in image_paths:
        image = cv2.imread(image_path)
        video_writer.write(image)

    video_writer.release()

# Streamlit app setup
st.sidebar.title("AI Video Generator")
st.sidebar.subheader("Enter Your OpenAI API Key")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

task = st.sidebar.radio("Select a task:", ["Generate Video from Text"])

if api_key and validate_openai_key(api_key):
    if task == "Generate Video from Text":
        st.subheader("🎬 Generate AI Video from Text:")
        video_prompt = st.text_area("Enter your video description:", "")

        if st.button("Generate Video"):
            if video_prompt.strip():
                with st.spinner("Generating video..."):
                    # Generate images based on the text prompt
                    image_paths = []
                    for _ in range(5):  # Generate 5 images based on text prompt
                        img_path = generate_image_from_text(api_key, video_prompt)
                        if img_path:  # Only append valid image paths
                            image_paths.append(img_path)

                    if image_paths:
                        # Create a video from the images
                        video_path = tempfile.mktemp(suffix=".mp4")
                        generate_video_from_images(image_paths, video_path)

                        # Display the video
                        st.success("Video Generated Successfully!")
                        st.video(video_path)
                    else:
                        st.error("No images were generated. Please check the error above.")
            else:
                st.warning("Please enter a video description.")
else:
    if api_key:
        st.warning("Invalid API key. Please check your key and try again.")
