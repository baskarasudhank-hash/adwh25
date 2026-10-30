"""
commands.py - Local (offline) commands.
These answers do not need the Z.ai API, so they reply instantly:
greeting, time, date, jokes, open websites, wikipedia, screenshot.
"""

import datetime
import os
import random
import webbrowser

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the computer go to the doctor? Because it caught a virus!",
    "Why do Java developers wear glasses? Because they cannot C sharp!",
    "What is a computer's first sign of old age? Loss of memory.",
    "Why was the mobile phone wearing glasses? It lost all its contacts.",
    "What did the router say to the doctor? It hurts when IP.",
    "Why did the student eat his homework? The teacher said it was a piece of cake!",
    "What do you call a fish without eyes? A fsh!",
]

WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "wikipedia": "https://www.wikipedia.org",
    "whatsapp": "https://web.whatsapp.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "github": "https://github.com",
    "stack overflow": "https://stackoverflow.com",
}


def get_greeting():
    """Return Good morning / Good afternoon / Good evening by clock time."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning"
    if hour < 17:
        return "Good afternoon"
    return "Good evening"


def _time_reply():
    now = datetime.datetime.now()
    return "The time is " + now.strftime("%I:%M %p")


def _date_reply():
    now = datetime.datetime.now()
    return "Today is " + now.strftime("%A, %d %B %Y")


def _open_website_reply(t):
    """If the user said: open youtube / open google ... return the reply."""
    for name, url in WEBSITES.items():
        if name in t and ("open" in t or "go to" in t):
            webbrowser.open(url)
            return "Opening " + name
    return None


def _search_reply(t):
    """If the user said: search for cats  -> open Google search."""
    if "search for" in t or t.startswith("search "):
        query = t.split("search for", 1)[-1].strip()
        if not query:
            query = t.replace("search", "", 1).strip()
        if query:
            webbrowser.open("https://www.google.com/search?q=" + query.replace(" ", "+"))
            return "Searching Google for " + query
    return None


def _youtube_search_reply(t):
    """If the user said: play songs on youtube -> open YouTube search."""
    if "on youtube" in t:
        query = t.split("on youtube", 1)[0].strip()
        for word in ("play", "search", "find", "open"):
            if query.startswith(word):
                query = query[len(word):].strip()
        if query:
            url = "https://www.youtube.com/results?search_query=" + query.replace(" ", "+")
            webbrowser.open(url)
            return "Playing " + query + " on YouTube"
    return None


def _wikipedia_reply(t):
    """If the user said: wikipedia india -> speak 2 sentences about india."""
    if "wikipedia" in t:
        topic = t.split("wikipedia", 1)[-1].strip()
        if not topic:
            return "Please tell the topic. Example: wikipedia India."
        try:
            import wikipedia
            summary = wikipedia.summary(topic, sentences=2, auto_suggest=True)
            return summary
        except Exception:
            return "Sorry, I could not find " + topic + " on Wikipedia."
    return None


def _screenshot_reply():
    folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(folder, "screenshot_" +
                        datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".png")
    try:
        import pyautogui
        pyautogui.screenshot(path)
        return "Screenshot saved in the project folder."
    except Exception:
        return "Sorry, screenshot failed on this computer."


def try_command(text, assistant_name="Nova"):
    """
    Check if the text is a local command.

    Returns a tuple (handled, reply, action):
        handled : True  -> reply is final, no need to call Z.ai
        reply   : text to show and speak
        action  : "none" | "exit" | "stop"
    """
    t = text.lower().strip()

    # ---- Exit words ----
    if t in ("exit", "quit", "bye", "goodbye", "close", "see you",
             "thank you bye"):
        return True, "Goodbye! Have a nice day!", "exit"

    # ---- Stop listening (like pressing the Stop button) ----
    if "stop listening" in t or t == "stop":
        return True, "Okay, I will stop listening.", "stop"

    # ---- Greeting words ----
    greeting_words = ("hello", "hi", "hey", "vanakkam")
    if any(g == t or t == g + " " + assistant_name.lower() for g in greeting_words):
        return True, get_greeting() + "! How can I help you?", "none"
    if t.startswith("good morning") or t.startswith("good afternoon") \
            or t.startswith("good evening"):
        return True, get_greeting() + "! How can I help you?", "none"

    # ---- Who are you ----
    if "who are you" in t or "your name" in t or "introduce yourself" in t:
        return True, ("I am " + assistant_name + ", your personal AI assistant, "
                      "powered by the Z.ai GLM model. I can answer questions, "
                      "tell time, open websites and more."), "none"

    # ---- Time ----
    if "time" in t and "timer" not in t:
        return True, _time_reply(), "none"

    # ---- Date / day ----
    if "date" in t or "what day" in t or ("today" in t and "day" in t):
        return True, _date_reply(), "none"

    # ---- Thank you ----
    if "thank you" in t or t == "thanks":
        return True, "You are welcome! Happy to help.", "none"

    # ---- Joke ----
    if "joke" in t or "make me laugh" in t:
        return True, random.choice(JOKES), "none"

    # ---- Screenshot ----
    if "screenshot" in t or "take a snap" in t:
        return True, _screenshot_reply(), "none"

    # ---- Websites / search ----
    reply = _open_website_reply(t)
    if reply:
        return True, reply, "none"
    reply = _youtube_search_reply(t)
    if reply:
        return True, reply, "none"
    reply = _search_reply(t)
    if reply:
        return True, reply, "none"

    # ---- Wikipedia ----
    reply = _wikipedia_reply(t)
    if reply:
        return True, reply, "none"

    # ---- Not a local command: let Z.ai answer ----
    return False, "", "none"
