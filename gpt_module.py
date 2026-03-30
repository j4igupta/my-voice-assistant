import time
from google import genai
from google.api_core import exceptions as errors
from config import OPENAI_API_KEY

# Use the new key you got from AI Studio
client = genai.Client(api_key=OPENAI_API_KEY)

def ask_gpt(prompt):
    # 'gemini-2.5-flash-lite' is the 2026 stable king for free-tier voice agents
    current_model = "gemini-2.5-flash-lite" 
    
    try:
        response = client.models.generate_content(
            model=current_model, 
            contents=prompt
        )
        reply = response.text
        print("AI:", reply)
        return reply
        
    except errors.ClientError as e:
        if "429" in str(e):
            print("System: Rate limit hit. Retrying in 10 seconds...")
            time.sleep(10) 
            return ask_gpt(prompt)
        else:
            print(f"API Error: {e}")
            return "Sir, there was a connection error."
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return "An unexpected error occurred."