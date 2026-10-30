"""
zai_brain.py - The brain of the assistant.
This file sends the user's question to the Z.ai GLM model
and returns the AI answer as text.
"""

import requests
import config

# We tell the AI how to behave. Short answers are best for voice.
SYSTEM_PROMPT = (
    "You are " + config.ASSISTANT_NAME + ", a friendly personal voice assistant "
    "for a college student. Answer in simple English. Keep answers short "
    "(2 to 4 sentences) because the answer will be spoken aloud. "
    "If the user asks for a list, give maximum 4 short points."
)


def ask_zai(question, history=None):
    """
    Send one question to Z.ai and return the answer text.

    history = past conversation, a list like:
        [{"role": "user", "content": "..."},
         {"role": "assistant", "content": "..."}]
    It lets the AI remember what you spoke before.
    """
    if not config.check_api_key():
        return ("API key is missing. Please open the .env file and paste your "
                "Z.ai API key. See README.md step 3 for help.")

    headers = {
        "Authorization": "Bearer " + config.ZAI_API_KEY,
        "Content-Type": "application/json",
        "Accept-Language": "en-US,en",
    }

    # Build the full message list: system + memory + new question
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history[-6:])          # remember last 6 messages
    messages.append({"role": "user", "content": question})

    body = {
        "model": config.ZAI_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 400,
    }

    try:
        response = requests.post(config.ZAI_API_URL,
                                 headers=headers, json=body, timeout=40)
        response.raise_for_status()
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        return answer.strip()

    except requests.exceptions.Timeout:
        return "Sorry, the Z.ai server took too long to reply. Please try again."
    except requests.exceptions.HTTPError:
        return ("Z.ai rejected the request. Please check your API key and the "
                "model name in the .env file, and your internet connection.")
    except requests.exceptions.ConnectionError:
        return "Internet connection problem. Please check your network."
    except Exception:
        return "Sorry, something went wrong while talking to Z.ai."
