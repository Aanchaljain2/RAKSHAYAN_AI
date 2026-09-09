import speech_recognition as sr
import pyttsx3


# -----------------------------
# TEXT TO SPEECH
# -----------------------------

engine = pyttsx3.init()

engine.setProperty("rate", 165)


def speak(text):
    print(f"Rakshayan AI: {text}")
    engine.say(text)
    engine.runAndWait()


# -----------------------------
# SPEECH TO TEXT
# -----------------------------

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("\n🎤 Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        except sr.WaitTimeoutError:
            print("❌ No speech detected.")
            return ""

    try:

        text = recognizer.recognize_google(audio)

        print(f"You said: {text}")

        return text.lower()

    except sr.UnknownValueError:

        print("❌ Could not understand.")

        return ""

    except sr.RequestError:

        print("❌ Speech recognition service unavailable.")

        return ""


# -----------------------------
# TEST
# -----------------------------

if __name__ == "__main__":

    speak("Hello. I am Rakshayan.")

    speak("Is there any issue or emergency?")

    command = listen()

    if command:
        speak(f"You said {command}")

    else:
        speak("I could not understand you.")