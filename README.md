# 📸 AI Hashtag Generator

A lightweight Flask web application that uses OpenAI's vision capabilities (`gpt-4o-mini`) to analyze uploaded images and automatically generate exactly 30 relevant social media hashtags.

## 🚀 Features
- **Image Upload:** Users can upload any standard image (`.jpg`/`.jpeg`) via a clean web interface.
- **Base64 Encoding:** Securely encodes images locally before transferring them to the API pipeline.
- **AI Vision Analysis:** Leverages OpenAI's `gpt-4o-mini` to look at the image and extract relevant keywords/hashtags.
- **Automatic Formatting:** Parses the comma-separated API response into a structured list ready to use.

## 🔧 Prerequisites & Installation

1. **Install Dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install flask requests python-dotenv