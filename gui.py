"""
gui.py - The Tkinter window of the assistant.

Shows: chat display, status, Start Listening / Stop / Exit buttons,
and a typing box (useful if the microphone is not available).
"""

import queue
import threading
import tkinter as tk
from tkinter import scrolledtext

import commands
import config
import speech_engine
from zai_brain import ask_zai

BG = "#F1F5F9"        # light gray background
HEADER_BG = "#0F172A" # dark blue header
USER_C = "#1D4ED8"    # blue for user text
BOT_C = "#047857"     # green for assistant text
SYS_C = "#6B7280"     # gray for system notes


class VoiceAssistantApp:
    """Main application class - builds the window and runs the logic."""

    def __init__(self, root):
        self.root = root
        self.root.title(config.ASSISTANT_NAME + " - AI Voice Assistant (Z.ai GLM)")
        self.root.geometry("780x620")
        self.root.minsize(640, 520)
        self.root.configure(bg=BG)

        # ---- state variables ----
        self.msg_queue = queue.Queue()       # worker threads talk to GUI through it
        self.stop_event = threading.Event()  # Stop button sets this
        self.is_listening = False            # is the listen loop running?
        self.history = []                    # short memory for Z.ai conversation

        self._build_widgets()
        self.root.after(100, self._poll_queue)
        self.root.after(600, self._welcome)

    # ------------------------------------------------------------------
    # WINDOW LAYOUT
    # ------------------------------------------------------------------
    def _build_widgets(self):
        header = tk.Frame(self.root, bg=HEADER_BG, height=64)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header,
                 text=config.ASSISTANT_NAME + "  |  AI Voice Assistant",
                 font=("Segoe UI", 17, "bold"),
                 bg=HEADER_BG, fg="#FFFFFF").pack(side="left", padx=18)

        self.status_label = tk.Label(header, text="Status: Starting...",
                                     font=("Segoe UI", 11),
                                     bg=HEADER_BG, fg="#7DD3FC")
        self.status_label.pack(side="right", padx=18)

        # ---- chat display ----
        self.chat = scrolledtext.ScrolledText(
            self.root, font=("Segoe UI", 11), bg="#FFFFFF", fg="#111827",
            wrap="word", state="disabled", relief="flat", padx=14, pady=10)
        self.chat.pack(fill="both", expand=True, padx=16, pady=12)
        self.chat.tag_configure("user", foreground=USER_C,
                                font=("Segoe UI", 11, "bold"))
        self.chat.tag_configure("bot", foreground=BOT_C)
        self.chat.tag_configure("system", foreground=SYS_C,
                                font=("Segoe UI", 10, "italic"))

        # ---- button row ----
        buttons = tk.Frame(self.root, bg=BG)
        buttons.pack(fill="x", padx=16)

        self.start_btn = tk.Button(
            buttons, text="Start Listening", font=("Segoe UI", 12, "bold"),
            bg="#16A34A", fg="white", activebackground="#15803D",
            activeforeground="white", relief="flat", padx=18, pady=8,
            cursor="hand2", command=self.start_listening)
        self.start_btn.pack(side="left")

        self.stop_btn = tk.Button(
            buttons, text="Stop", font=("Segoe UI", 12, "bold"),
            bg="#DC2626", fg="white", activebackground="#B91C1C",
            activeforeground="white", relief="flat", padx=18, pady=8,
            cursor="hand2", command=self.stop_listening)
        self.stop_btn.pack(side="left", padx=10)

        exit_btn = tk.Button(
            buttons, text="Exit", font=("Segoe UI", 12),
            bg="#475569", fg="white", activebackground="#334155",
            activeforeground="white", relief="flat", padx=18, pady=8,
            cursor="hand2", command=self.close_app)
        exit_btn.pack(side="right")

        # ---- typing row (backup if no microphone) ----
        typing = tk.Frame(self.root, bg=BG)
        typing.pack(fill="x", padx=16, pady=(6, 4))

        self.entry = tk.Entry(typing, font=("Segoe UI", 11), relief="flat",
                              bg="#FFFFFF", fg="#111827")
        self.entry.pack(side="left", fill="x", expand=True, ipady=7, ipadx=4)
        self.entry.bind("<Return>", self.send_typed)

        send_btn = tk.Button(
            typing, text="Send", font=("Segoe UI", 11, "bold"),
            bg="#2563EB", fg="white", activebackground="#1D4ED8",
            activeforeground="white", relief="flat", padx=16,
            cursor="hand2", command=self.send_typed)
        send_btn.pack(side="left", padx=(8, 0))

        tk.Label(typing, text="No microphone? Type here.",
                 font=("Segoe UI", 9), bg=BG, fg=SYS_C).pack(side="left", padx=(8, 0))

    # ------------------------------------------------------------------
    # DISPLAY HELPERS (only the GUI thread may touch the widgets)
    # ------------------------------------------------------------------
    def _show(self, who, text):
        tag = {"You": "user", config.ASSISTANT_NAME: "bot"}.get(who, "system")
        prefix = "You: " if who == "You" else \
                 (config.ASSISTANT_NAME + ": " if who == config.ASSISTANT_NAME else "")
        self.chat.configure(state="normal")
        self.chat.insert("end", prefix + text + "\n\n", tag)
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def _set_status(self, text):
        self.status_label.config(text="Status: " + text)

    # ------------------------------------------------------------------
    # EVENTS
    # ------------------------------------------------------------------
    def _welcome(self):
        greeting = commands.get_greeting()
        self._show("system", "Welcome! Press 'Start Listening' and speak, "
                             "or type your question below.")
        if not config.check_api_key():
            self._show("system", "Warning: API key not found in the .env file. "
                                 "Z.ai answers will not work. Read README.md step 3.")
        text = (greeting + "! I am " + config.ASSISTANT_NAME +
                ", your AI assistant. How can I help you?")
        self._show(config.ASSISTANT_NAME, text)
        threading.Thread(target=speech_engine.speak, args=(text,),
                         daemon=True).start()

    def start_listening(self):
        if self.is_listening:
            return
        self.is_listening = True
        self.stop_event.clear()
        self.start_btn.config(state="disabled", bg="#6B7280")
        threading.Thread(target=self._listen_loop, daemon=True).start()

    def stop_listening(self):
        self.stop_event.set()
        speech_engine.stop_speaking()
        self._set_status("Stopped. Press Start to talk again.")

    def send_typed(self, event=None):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        self.msg_queue.put(("user", text))
        threading.Thread(target=self._handle_question, args=(text,),
                         daemon=True).start()

    def close_app(self):
        self.stop_event.set()
        speech_engine.stop_speaking()
        self.root.after(200, self.root.destroy)

    # ------------------------------------------------------------------
    # BACKGROUND WORK (runs in worker threads, never touches widgets)
    # ------------------------------------------------------------------
    def _listen_loop(self):
        """Keep listening until the user presses Stop or says exit."""
        while not self.stop_event.is_set():
            self.msg_queue.put(("status", "Listening... speak now"))
            text = speech_engine.listen(timeout=6, phrase_time_limit=20)
            if self.stop_event.is_set():
                break
            if text is None:
                self.msg_queue.put(("system",
                                    "Speech service not reachable. "
                                    "Check your internet connection."))
                continue
            if text == "":
                self.msg_queue.put(("status", "I did not hear anything..."))
                continue
            self.msg_queue.put(("user", text))
            self._handle_question(text)
        self.msg_queue.put(("status", "Idle. Press Start Listening."))
        self.msg_queue.put(("enable_start", ""))

    def _handle_question(self, text):
        """One question = local command first, if not then Z.ai."""
        handled, reply, action = commands.try_command(text, config.ASSISTANT_NAME)
        if handled:
            self.msg_queue.put(("bot", reply))
            self._remember(text, reply)
            speech_engine.speak(reply)
            if action == "exit":
                self.msg_queue.put(("exit", ""))
            elif action == "stop":
                self.stop_event.set()
                self.msg_queue.put(("enable_start", ""))
            return

        self.msg_queue.put(("status", "Thinking... asking Z.ai"))
        answer = ask_zai(text, self.history)
        self.msg_queue.put(("bot", answer))
        self._remember(text, answer)
        speech_engine.speak(answer)

    def _remember(self, question, answer):
        self.history.append({"role": "user", "content": question})
        self.history.append({"role": "assistant", "content": answer})
        if len(self.history) > 12:          # keep memory small
            self.history = self.history[-12:]

    # ------------------------------------------------------------------
    # QUEUE PUMP: safely moves data from worker threads into the GUI
    # ------------------------------------------------------------------
    def _poll_queue(self):
        try:
            while True:
                kind, payload = self.msg_queue.get_nowait()
                if kind == "user":
                    self._show("You", payload)
                elif kind == "bot":
                    self._show(config.ASSISTANT_NAME, payload)
                elif kind == "system":
                    self._show("system", payload)
                elif kind == "status":
                    self._set_status(payload)
                elif kind == "enable_start":
                    self.is_listening = False
                    self.start_btn.config(state="normal", bg="#16A34A")
                elif kind == "exit":
                    self.close_app()
                    return
        except queue.Empty:
            pass
        self.root.after(100, self._poll_queue)
