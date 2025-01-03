import requests
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, AudioFileClip
from gtts import gTTS
import librosa
import openai
from dotenv import load_dotenv
import os

# Load API keys
load_dotenv()
pexels_api_key = os.getenv("Yp8EBP8TIJmNC0x6C1lbAxHz2VNfFB3sJvO4rTLp8s1OlpZMyH2cWm7k")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to fetch Pexels video
def fetch_pexels_video(query):
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=1"
    headers = {"Authorization": pexels_api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        video_url = data['videos'][0]['video_files'][0]['link']
        return video_url
    return None

# Function to generate script using OpenAI
def generate_script(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Function to convert text to speech
def text_to_speech(text, output_file):
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)

# Function to combine video, audio, and text
def combine_elements(video_url, audio_path, script, output_file):
    # Download the video from Pexels (simple method)
    video_clip = VideoFileClip(video_url).subclip(0, 10)  # First 10 seconds
    text_clip = TextClip(script, fontsize=24, color='white').set_position('center').set_duration(10)
    voiceover = AudioFileClip(audio_path)
    
    # Combine video, text, and audio
    final_clip = concatenate_videoclips([video_clip])
    final_clip = final_clip.set_audio(voiceover)
    final_clip.write_videofile(output_file)

# Example usage
def create_video(prompt, audio_file):
    # Step 1: Fetch Video
    video_url = fetch_pexels_video("sunset")
    if not video_url:
        print("Error fetching video")
        return
    
    # Step 2: Generate Script
    script = generate_script(prompt)
    
    # Step 3: Generate Voiceover
    text_to_speech(script, "voiceover.mp3")
    
    # Step 4: Combine Elements
    combine_elements(video_url, audio_file, script, "final_output.mp4")

# Create a video
create_video("Create a relaxing video about sunsets", "background_music.mp3")
