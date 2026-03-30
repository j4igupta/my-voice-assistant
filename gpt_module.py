import time
from google import genai
from google.genai import types
from google.api_core import exceptions as errors
from config import OPENAI_API_KEY
from PIL import Image

client = genai.Client(api_key=OPENAI_API_KEY)

MODEL = "gemini-2.5-flash-lite"

# Smart glasses / voice assistant system prompt
SYSTEM_PROMPT = """You are an intelligent AI assistant built into a pair of smart glasses. 
You respond conversationally and concisely — answers should be spoken aloud, so avoid 
bullet points, markdown, or long lists. Prioritize clarity and brevity. 
For vision queries, describe what you see in plain natural language as if guiding someone."""


def ask_gpt(prompt: str, retries: int = 3) -> str:
    """Send a text prompt to Gemini and return the spoken response."""
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                ),
                contents=prompt
            )
            reply = response.text.strip()
            print(f"AI: {reply}")
            return reply

        except errors.ClientError as e:
            if "429" in str(e):
                wait = 10 * (attempt + 1)  # FIX: no recursion — iterative backoff
                print(f"Rate limit hit. Waiting {wait}s... (attempt {attempt+1}/{retries})")
                time.sleep(wait)
            else:
                print(f"API Error: {e}")
                return "Sorry, there was a connection error."

        except Exception as e:
            print(f"Unexpected error: {e}")
            return "An unexpected error occurred."

    return "I'm being rate limited. Please try again in a moment."


def ask_vision(prompt: str, image_path: str, retries: int = 3) -> str:
    """Send an image + text prompt to Gemini Vision and return the spoken response.
    
    FIX: The plan's code used the old google.generativeai SDK. This repo uses
    the new google.genai client — the APIs are incompatible. This uses the
    correct new-SDK approach with types.Part.
    """
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Failed to open image: {e}")
        return "I couldn't read the camera image."

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.4,  # lower temp for factual vision descriptions
                ),
                contents=[
                    types.Part.from_image(image),
                    prompt
                ]
            )
            reply = response.text.strip()
            print(f"AI (vision): {reply}")
            return reply

        except errors.ClientError as e:
            if "429" in str(e):
                wait = 10 * (attempt + 1)
                print(f"Rate limit hit. Waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"Vision API Error: {e}")
                return "Sorry, I had trouble analyzing the image."

        except Exception as e:
            print(f"Unexpected vision error: {e}")
            return "I couldn't process what I saw."

    return "I'm being rate limited. Please try again in a moment."
