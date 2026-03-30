from wake import listen_for_wake
from stt import listen
from gpt_module import ask_gpt, ask_vision
from tts import speak
from vision import capture_image

# Keywords that trigger the vision pipeline
VISION_TRIGGERS = {"look", "see", "show", "what", "read", "scan", "describe", "danger", "hazard"}

# Map specific words to targeted vision prompts
VISION_PROMPTS = {
    "read":    "Read any visible text in this image clearly.",
    "danger":  "Identify any hazards or dangerous objects in this image immediately.",
    "hazard":  "Identify any hazards or dangerous objects in this image immediately.",
    "objects": "List the key objects you can see in this image.",
    "scan":    "Give a quick summary of everything visible in this image.",
}

DEFAULT_VISION_PROMPT = (
    "You are an assistant for smart glasses. "
    "Briefly describe the most important things in front of the user in one or two sentences."
)


def get_vision_prompt(text: str) -> str:
    """Pick the most specific vision prompt based on what the user said."""
    words = text.lower().split()
    for word in words:
        if word in VISION_PROMPTS:
            return VISION_PROMPTS[word]
    return DEFAULT_VISION_PROMPT


def is_vision_request(text: str) -> bool:
    """Check if the user's words suggest they want visual analysis."""
    words = set(text.lower().split())
    return bool(words & VISION_TRIGGERS)


def main():
    print("Smart glasses assistant ready. Say 'Jarvis' to activate.")

    while True:
        # Step 1: Wait for wake word
        listen_for_wake()

        # Step 2: Listen for the command
        text = listen()
        if not text:
            continue

        print(f"You: {text}")

        # Step 3: Route to vision or text pipeline
        if is_vision_request(text):
            speak("Looking.")
            image_path = capture_image()

            if image_path:
                prompt = get_vision_prompt(text)
                response = ask_vision(prompt, image_path)
            else:
                response = "Camera error. I couldn't capture an image."
        else:
            response = ask_gpt(text)

        # Step 4: Speak the response
        speak(response)


if __name__ == "__main__":
    main()
