# Nova - AI Personal Voice Assistant (Z.ai + Python)

A working college project prototype. You speak, Nova answers with voice.
The AI answers come from the **Z.ai GLM** model through its API.

---
தமிழ்: இது ஒரு முழுமையான கல்லூரி திட்டம். நீங்கள் பேசினால், Nova குரலில் பதில் சொல்லும். AI பதில்கள் Z.ai GLM மாடலிடமிருந்து வரும்.

---

## 1. What this project does

1. Listens to your voice through the **microphone**
2. Converts your speech into **text** (SpeechRecognition)
3. Sends the question to **Z.ai GLM** and gets an AI answer
4. Speaks the answer through the **speakers** (pyttsx3)
5. Shows everything on a **Tkinter window**

Extra features: greeting, date, time, jokes, open websites,
Google / YouTube search, Wikipedia summary, screenshot.

---
தமிழ்: மைக் வழியாகக் கேட்கும், உரையாக மாற்றும், Z.ai-யிடம் கேள்வியை அனுப்பும், பதிலை ஒலிக்கொண்டு சொல்லும். வணக்கம், தேதி, நேரம், ஜோக்குகள், இணையதளம் திறத்தல் போன்ற அம்சங்களும் உண்டு.

---

## 2. Folder structure

```
AI_Voice_Assistant/
|-- main.py            Start point. Run this file.
|-- gui.py             Tkinter window (buttons, chat display)
|-- speech_engine.py   listen() = mic to text, speak() = text to voice
|-- commands.py        Local commands (time, date, jokes, websites...)
|-- zai_brain.py       Sends questions to Z.ai GLM API
|-- config.py          Reads the .env file and settings
|-- requirements.txt   List of libraries to install
|-- .env.example       Sample secret file (rename it to .env)
|-- run.bat            Double-click to start (Windows)
|-- test_offline.py    Quick test without microphone and API
`-- README.md          This guide
```

---

## 3. Installation (Windows, step by step)

### Step 1 - Install Python
- Download Python 3.10 or newer from https://www.python.org/downloads/
- IMPORTANT: tick the checkbox **"Add Python to PATH"** during installation.
- Check: open Command Prompt and type `python --version`

தமிழ்: Python நிறுவும்போது **"Add Python to PATH"** என்ற பெட்டியை கண்டிப்பாக டிக் செய்யவும்.

### Step 2 - Get your Z.ai API key (free)
1. Open https://z.ai/model-api in your browser
2. Click **Register / Login** and create an account
3. Open the **API Keys** page: https://z.ai/manage-apikey/apikey-list
4. Click **Create API Key**, copy the key (it looks like `xxxxxxxx.xxxxxxxxx`)

தமிழ்: z.ai-யில் கணக்கு உருவாக்கி, API Keys பக்கத்தில் புதிய key உருவாக்கி copy செய்யவும்.

### Step 3 - Create the .env file (protects your key)
1. In the project folder, rename `.env.example` to `.env`
2. Open it with Notepad and paste your key:

```
ZAI_API_KEY=paste_your_real_key_here
ZAI_MODEL=glm-5.3-flash
```

3. Save and close. Never share this file, never upload it to GitHub.

தமிழ்: `.env.example` கோப்பை `.env` என மறுபெயரிட்டு, உங்கள் key-ஐ ஒட்டவும். இந்த கோப்பை யாருடனும் பகிர வேண்டாம்.

### Step 4 - Install the libraries
Open Command Prompt **inside the project folder**, then type:

```
pip install -r requirements.txt
```

If `pyaudio` gives an error, try:

```
pip install pipwin
pipwin install pyaudio
```

தமிழ்: `pip install -r requirements.txt` என்ற கட்டளையால் தேவையான நூலகங்கள் அனைத்தும் நிறுவப்படும். pyaudio பிழை வந்தால் மேலே உள்ள கட்டளைகளை முயற்சிக்கவும்.

### Step 5 - Run the project

Option A: double-click `run.bat`
Option B: in Command Prompt type:

```
python main.py
```

A window opens. Nova greets you. Press **Start Listening** and speak!

---

## 4. Voice commands you can try

| You say | Nova does |
|---|---|
| "Hello" | Greets you back |
| "What is the time" | Speaks the current time |
| "What is the date today" | Speaks today's date |
| "Tell me a joke" | Speaks a funny joke |
| "Open YouTube" / "Open Google" | Opens the website |
| "Search for AI news" | Opens Google search |
| "Play songs on YouTube" | Opens YouTube search |
| "Wikipedia India" | 2 sentence summary of India |
| "Screenshot" | Saves a screenshot PNG |
| Any general knowledge question | Z.ai GLM answers |
| "Stop listening" / press Stop | Stops the microphone |
| "Bye" | Closes the app |

No microphone? Type the same text in the box and press **Send**.

---

## 5. Testing

1. Run `python test_offline.py` - tests all local commands (no mic, no API needed)
2. Run the app and try: time, date, joke (local commands)
3. Type "Explain black holes" and press Send - tests the Z.ai API
4. Press Start Listening and say "hello" - tests the microphone

---

## 6. Troubleshooting

| Problem | Fix |
|---|---|
| "pyaudio not found" | `pip install pipwin` then `pipwin install pyaudio` |
| Mic does not listen | Windows Settings -> Privacy -> Microphone -> allow desktop apps |
| No voice heard | Check speaker volume; Windows Settings -> Sound -> choose output |
| "API key is missing" | .env file missing or key not pasted. Redo Step 3 |
| Z.ai rejects request | Check the key, check `ZAI_MODEL` name, check internet |
| Speech not accurate | Speak clearly, reduce background noise; try `en-US` in speech_engine.py |

---

## 7. Put the project on GitHub

This folder is already a Git repository with clean commits.
To upload it: create an empty repo on GitHub, then run:

```
git remote add origin https://github.com/YOUR-USERNAME/AI-Voice-Assistant.git
git push -u origin main
```

Full beginner guide: see **HOW_TO_PUSH_TO_GITHUB.md** (English + Tamil).

தமிழ்: GitHub-இல் பதிவேற்றும் முழு வழிமுறைகள் `HOW_TO_PUSH_TO_GITHUB.md` கோப்பில் உள்ளது.

---

## 8. Safety notes

- The API key is stored only in the `.env` file on your computer.
- `.gitignore` blocks `.env`, so the key can never be uploaded to GitHub.
- SpeechRecognition uses Google's free web speech service, so internet is needed for listening.
- pyttsx3 voice output works fully offline.
