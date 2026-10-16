
import os
import secrets
import time
import threading

from collections import deque
from flask import Flask, render_template, request, jsonify, session
from ollama import chat

app = Flask(__name__)

# Use a stable secret key when deploying.
# A temporary key is generated for local testing.
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    secrets.token_hex(32)
)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

MODEL = "gemma4"
MAX_MESSAGE_LENGTH = 2000
MAX_HISTORY_MESSAGES = 12

SYSTEM_PROMPT = """
You are Muneeb AI, a friendly and helpful assistant.
Answer clearly and intelligently.
Explain difficult concepts in simple language.
Use examples when helpful.
If you are unsure, say so honestly.
"""

# In-memory storage for this demonstration.
conversations = {}
request_times = {}
storage_lock = threading.Lock()
ai_lock = threading.Lock()


def get_chat_id():
    if "chat_id" not in session:
        session["chat_id"] = secrets.token_urlsafe(24)

    return session["chat_id"]


def get_history(chat_id):
    with storage_lock:
        if chat_id not in conversations:
            conversations[chat_id] = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ]

        return conversations[chat_id]


def allow_request(chat_id):
    now = time.time()

    with storage_lock:
        times = request_times.setdefault(chat_id, deque())

        while times and now - times[0] > 60:
            times.popleft()

        if len(times) >= 8:
            return False

        times.append(now)
        return True


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/chat")
def chat_route():
    data = request.get_json(silent=True) or {}
    user_text = data.get("message", "")

    if not isinstance(user_text, str):
        return jsonify({"error": "Message must be text."}), 400

    user_text = user_text.strip()

    if not user_text:
        return jsonify({"error": "Please type a message."}), 400

    if len(user_text) > MAX_MESSAGE_LENGTH:
        return jsonify({
            "error": "Message is too long. Use under 2000 characters."
        }), 400

    chat_id = get_chat_id()

    if not allow_request(chat_id):
        return jsonify({
            "error": "Too many messages. Please wait a minute."
        }), 429

    # Serialize calls because this demo uses one local AI model.
    with ai_lock:
        history = get_history(chat_id)

        history.append({
            "role": "user",
            "content": user_text
        })

        try:
            response = chat(
                model=MODEL,
                messages=history
            )

            answer = response.message.content

            history.append({
                "role": "assistant",
                "content": answer
            })

            # Keep recent messages plus the system instructions.
            if len(history) > MAX_HISTORY_MESSAGES + 1:
                conversations[chat_id] = (
                    [history[0]] +
                    history[-MAX_HISTORY_MESSAGES:]
                )

            return jsonify({"reply": answer})

        except Exception:
            history.pop()
            app.logger.exception("AI request failed")

            return jsonify({
                "error": (
                    "AI is unavailable. Check Ollama and your model."
                )
            }), 503


@app.post("/clear")
def clear_chat():
    chat_id = session.get("chat_id")

    if chat_id:
        with ai_lock:
            with storage_lock:
                conversations.pop(chat_id, None)
                request_times.pop(chat_id, None)

    session.pop("chat_id", None)

    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
