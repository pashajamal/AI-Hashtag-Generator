import os

from flask import Flask, render_template, request, jsonify
import base64
import requests
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file (e.g. OPENAI_KEY)
load_dotenv()


def encode_image(image_path):
    """Read an image file from disk and return its Base64-encoded string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


@app.route('/', methods=['GET', 'POST'])
def index():
    base64_image = None

    if request.method == 'POST':
        # Retrieve the uploaded image from the form submission
        image = request.files['image']

        # Save the uploaded image temporarily to disk for encoding
        image.save("uploaded_image.jpg")

        # Encode the saved image to Base64 so it can be sent inline via the API
        base64_image = encode_image("uploaded_image.jpg")

        # Set request headers: JSON content type + Bearer token auth
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('OPENAI_KEY')}"
        }

        # Build the chat completion payload:
        # - System prompt locks the model into
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a hashtag generation model. "
                        "When you get an image as input, your response should always "
                        "contain exactly 30 hashtags separated by commas."
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Provide the hashtags for this image:"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            # Cap token usage — 30 short hashtags fit well within 300 tokens
            "max_tokens": 300
        }

        # Send the request to OpenAI's chat completions endpoint
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )

        # Extract the assistant's reply and split on commas to get individual hashtags
        # e.g. "#nature, #sunset, ..." → ['#nature', ' #sunset', ...]
        hashtags = (
            response.json()
            .get("choices")[0]
            .get("message")
            .get("content")
            .split(',')
        )

        # Re-render the page with the hashtag list and the image preview (Base64)
        return render_template('index.html', hashtags=hashtags, base64_image=base64_image)

    # GET request: render the empty form with no hashtags
    return render_template('index.html', hashtags=None)

if __name__ == '__main__':
    app.run(debug=True)
