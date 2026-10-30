"""
speech_engine.py - The ears and the mouth of the assistant.

1) listen() : Microphone  -> text     (uses the SpeechRecognition library)
2) speak()  : Text        -> speaker  (uses the pyttsx3 library, offline TTS)
"""

import threading

import pyttsx3
import speech_recognition as sr

import config

# Keeps the engine of the current speech, so the Stop button can stop it
_current_engine = None
_engine_lock = threading.Lock()


def speak(text):
    """Speak the given text through the laptop speakers."""
    global _current_engine
    if not text:
        return
    with _engine_lock:
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", config.VOICE_RATE)
            _current_engine = engine
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception:
            pass                      # never crash the app because of audio
        finally:
            _current_engine = None


def stop_speaking():
    """Stop the current speech. Used by the Stop button."""
    with _engine_lock:
        if _current_engine is not None:
            try:
                _current_engine.stop()
            except Exception:
                pass


def listen(timeout=6, phrase_time_limit=20):
    """
    Listen through the microphone and return the recognized English text.

    Returns:
        a string  -> what the user said
        ""        -> heard nothing / could not understand / no microphone
        None      -> internet problem with the speech service
    """
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source,
                                      timeout=timeout,
                                      phrase_time_limit=phrase_time_limit)
    except OSError:
        return ""                 # no microphone found on this computer

    try:
        # "en-IN" = Indian English. Change to "en-US" if needed.
        text = recognizer.recognize_google(audio, language="en-IN")
        return text
    except sr.UnknownValueError:
        return ""                 # speech was not clear
    except sr.RequestError:
        return None               # Google speech service not reachable
