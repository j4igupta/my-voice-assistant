from wake import listen_for_wake
from stt import listen
from gpt_module import ask_gpt
from tts import speak

def main():
    while True:
        listen_for_wake()

        text = listen()
        if not text:
            continue

        response = ask_gpt(text)
        speak(response)

if __name__ == "__main__":
    main()