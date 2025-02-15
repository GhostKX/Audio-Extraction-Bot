# Audio Extraction Bot


import telebot
import os
import logging
import requests
import subprocess
from moviepy.video.io.VideoFileClip import VideoFileClip
from dotenv import load_dotenv


# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


# Load environment variables from .env file
load_dotenv()
API_KEY = str(os.getenv('API_KEY'))
bot = telebot.TeleBot(API_KEY)


# Temporary directories for storing files
TEMP_DIR = './temp_files'
AUDIO_DIR = './audio_files'
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Welcome! 🎥🎧\n"
        "Send me a video, and I'll extract the audio for you.\n"
        "If the video exceeds 20MB, I'll split it into smaller parts, extract audio from each, and merge them seamlessly!"
    )


@bot.message_handler(content_types=['video', 'document'])
def handle_video(message):
    try:
        if message.content_type == 'video':
            file_id = message.video.file_id
            file_size = message.video.file_size
            file_name = f"{file_id}.mp4"
        elif message.content_type == 'document' and message.document.mime_type.startswith('video/'):
            file_id = message.document.file_id
            file_size = message.document.file_size
            file_name = message.document.file_name
        else:
            bot.send_message(message.chat.id, "❌ Please send a valid video file.")
            return

        # Download the file
        bot.send_message(message.chat.id, "📥 Downloading your video...")
        file_path = os.path.join(TEMP_DIR, file_name)
        print(file_path)
        download_video(file_id, file_path)

        # Check video size and process accordingly
        if file_size > 20 * 1024 * 1024:  # File size exceeds 20MB
            bot.send_message(message.chat.id, "🚨 File size exceeds 20MB. Splitting the video into parts...")
            audio_path = process_large_video(file_path)
        else:
            bot.send_message(message.chat.id, "🎧 Extracting audio...")
            audio_path = extract_audio(file_path)

        # Send the audio file back to the user
        with open(audio_path, 'rb') as audio_file:
            bot.send_audio(message.chat.id, audio_file)

        # Clean up temporary files
        cleanup([file_path, audio_path])
        bot.send_message(message.chat.id, "✅ Audio extracted successfully!")

    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)
        bot.send_message(message.chat.id, f"❌ An error occurred: {e}")


def download_video(file_id, save_path):
    """Download the video file from Telegram."""
    try:
        file_info = bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"

        with requests.get(file_url, stream=True) as response:
            response.raise_for_status()
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):  # 8 KB chunks
                    file.write(chunk)

        logging.info(f"Downloaded file to {save_path}")
    except Exception as e:
        logging.error(f"Failed to download file: {e}")
        raise


def process_large_video(video_path):
    """Split the video into smaller parts, extract audio from each, and merge the audio files."""
    video_clip = VideoFileClip(video_path)
    duration = video_clip.duration
    chunk_duration = 60  # 1 minute in seconds
    chunks = []
    start_time = 0
    chunk_count = 0

    # Splitting video into smaller chunks
    while start_time < duration:
        end_time = min(start_time + chunk_duration, duration)
        chunk_file = os.path.join(TEMP_DIR, f"chunk_{chunk_count}.mp4")
        video_clip.subclip(start_time, end_time).write_videofile(chunk_file, codec="libx264", audio_codec="aac")
        chunks.append(chunk_file)
        start_time = end_time
        chunk_count += 1

    audio_files = []

    # Extract audio from each chunk
    for i, chunk in enumerate(chunks):
        audio_file = os.path.join(AUDIO_DIR, f"audio_{i}.mp3")
        subprocess.run(['ffmpeg', '-i', chunk, '-vn', '-acodec', 'libmp3lame', '-ab', '128k', audio_file], check=True)
        audio_files.append(audio_file)

    # Merge all audio files
    final_audio_path = os.path.join(TEMP_DIR, "final_audio.mp3")
    merge_audio_files(audio_files, final_audio_path)

    # Cleanup individual chunks and audio files
    cleanup(chunks + audio_files)

    return final_audio_path


def extract_audio(video_path):
    """Extract audio from a single video file."""
    audio_path = os.path.join(TEMP_DIR, "audio.mp3")
    try:
        subprocess.run(
            ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'libmp3lame', '-ab', '128k', audio_path],
            check=True
        )
        return audio_path
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to extract audio: {e}")
        raise


def merge_audio_files(audio_files, output_path):
    """Merge multiple audio files into one using FFmpeg."""
    with open("audio_list.txt", "w") as f:
        for audio_file in audio_files:
            f.write(f"file '{os.path.abspath(audio_file)}'\n")

    subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'audio_list.txt', '-c', 'copy', output_path], check=True)
    os.remove("audio_list.txt")


def cleanup(files):
    """Delete temporary files."""
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            logging.info(f"Deleted temporary file: {file}")


# Start polling for messages
bot.polling(non_stop=True)
