# 🎧 Audio Extraction Bot  

A **Python-based Telegram bot** that extracts audio from videos. Users can send a video file, and the bot will **convert it into an MP3 file**. If the video exceeds **20MB**, the bot will **split it into smaller parts**, extract audio from each, and **merge them seamlessly**.  

Built using **PyTelegramBotAPI**, **MoviePy**, and **FFmpeg**, this bot ensures **high-quality audio extraction** with automated processing.  

---

## Features  

### 🎥 Video to Audio Conversion  
- **Extract High-Quality MP3 Audio** from videos  
- **Supports Large Videos** (Split and Merge Mechanism)  
- **Processes Video Files up to Any Size**  
- **Automated Handling for Big Files**  
- **Fast and Efficient Audio Extraction**  

### 📂 File Support  
- **Supports Any Video Format** (MP4, AVI, MKV, etc.)  
- **Handles Telegram Video Messages & Document Uploads**  
- **Saves Extracted Audio for Easy Access**  

### ✅ User-Friendly Features  
- **Simple Telegram Commands**  
- **Automated File Processing**  
- **Error Handling for Smooth Experience**  

---

## Requirements  

- **Python 3.x**  
- **Google Chrome & Chrome WebDriver**  
- **Libraries:**  
  - `telebot` (Telegram API)  
  - `moviepy` (Video Processing)  
  - `requests` (Downloading Files)  
  - `subprocess` (FFmpeg Integration)  
  - `dotenv` (Environment Variables)  

- **FFmpeg Installed** (Required for audio extraction)  

---

## 🛠 Installation  

1. Clone the Repository  
```bash
git clone https://github.com/GhostKX/Audio-Extraction-Bot.git

```

2. Install required dependencies
```bash
pip install -r requirements.txt
```

3. Configure the bot

- Create a .env file to store your Telegram API Key and OpenWeatherMap API Key
- Add your Telegram Bot Token:

```
API_KEY=your-telegram-bot-token
```

4. Navigate to the project directory
```bash
cd Audio-Exraction-Bot
```

5. Run the bot
```bash
python PythonAudioExtraction_bot.py
```

---

## Usage  

### Sending a Video  
- Start the bot by sending `/start`  
- Upload a **video file** in Telegram  
- The bot **downloads the video** and starts processing  

### Audio Extraction Process  
- If the video is **less than 20MB**, audio is extracted **directly**  
- If the video is **larger than 20MB**, the bot **splits it into smaller parts**, extracts audio, and **merges them**  

### Receiving the Audio File  
- Once processing is complete, the bot **sends back the MP3 file**  
- The original **video file is deleted** to save storage  


### Example Output:  

```
📥 Downloading your video...

🎧 Extracting audio...

✅ Audio extracted successfully!

🔊 Here’s your MP3 file! 🎶
```

---

## Author

- Developed by **GhostKX**
- GitHub: **[GhostKX](https://github.com/GhostKX/Audio-Extraction-Bot)**