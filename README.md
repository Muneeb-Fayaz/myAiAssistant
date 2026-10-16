# 🤖 Muneeb AI — Personal AI Assistant

> A fully self-built AI chat assistant powered by a local LLM, wrapped in a clean dark-mode web interface, and live on the internet.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-purple)
![Cloudflare](https://img.shields.io/badge/Cloudflare-Tunnel-orange?logo=cloudflare&logoColor=white)

---

## 📖 About the Project

**Muneeb AI** is a personal AI assistant I built from scratch in a single day. Instead of relying on a paid cloud API, it runs a large language model **locally through Ollama**, serves it with a **Flask** backend, and presents it through a modern chat interface. With a **Cloudflare Tunnel**, the assistant is accessible live from anywhere, straight from my own machine.

The idea was simple: create my own AI that I fully control, with no API keys, no usage bills, and complete privacy over conversations.

---

## ✨ Features

- 💬 **Real-time chat interface**: clean, responsive, dark-themed UI
- 🧠 **Local LLM inference**: powered by Ollama, so your data stays on your machine
- ⚡ **Lightweight Flask backend**: simple REST endpoint connecting the UI to the model
- 🌍 **Publicly accessible**: exposed securely online via Cloudflare Tunnel
- 🧹 **Clear chat button**: reset the conversation anytime
- 🟢 **Live status indicator**: shows when the assistant is online
- 🔒 **Private by design**: no third-party AI API involved

---

## 🛠️ Tech Stack

| Layer      | Technology                    |
|------------|-------------------------------|
| Language   | Python                        |
| Backend    | Flask                         |
| AI Engine  | Ollama (local LLM)            |
| Frontend   | HTML, CSS, JavaScript         |
| Deployment | Cloudflare Tunnel (cloudflared) |

---

## 🏗️ How It Works

```
 User (Browser)
       │
       ▼
 Cloudflare Tunnel  ──►  Public URL
       │
       ▼
 Flask Server (Python)
       │
       ▼
 Ollama (Local LLM)
       │
       ▼
 Response  ──►  Chat UI
```

1. The user types a message in the web interface.
2. The message is sent to the Flask backend.
3. Flask forwards the prompt to the Ollama model running locally.
4. The model's reply is returned and displayed in the chat window.
5. Cloudflare Tunnel makes the whole thing reachable over the internet.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com) installed
- [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) (optional, for public access)

### Installation

**1. Clone the repository**

```bash
git clone <your-repo-url>
cd muneeb-ai
```

**2. Install dependencies**

```bash
pip install flask requests
```

**3. Pull a model with Ollama**

```bash
ollama pull <model-name>
```

**4. Start Ollama**

```bash
ollama serve
```

**5. Run the Flask app**

```bash
python app.py
```

Open your browser at `http://localhost:5000` and start chatting.

### 🌐 Make It Live with Cloudflare

```bash
cloudflared tunnel --url http://localhost:5000
```

Cloudflare will generate a public URL you can share with anyone.

---

## 📂 Project Structure

```
muneeb-ai/
├── app.py            # Flask backend
├── templates/
│   └── index.html    # Chat UI
├── static/           # CSS / JS assets
└── README.md
```

> Adjust the structure above to match your actual files.

---

## 🔮 Future Improvements

- [ ] Conversation memory across sessions
- [ ] Streaming responses (typing effect)
- [ ] Markdown and code-block rendering
- [ ] Model selection dropdown
- [ ] User authentication
- [ ] Chat history export

---

## 📬 Contact & Resources

Have questions, feedback, or want to collaborate? I'd love to hear from you.

Reach out to me **directly on LinkedIn**:

👉 **[Muneeb Fayaz on LinkedIn](https://www.linkedin.com/in/muneeb-fayaz-0440823a4/)**

---

## 👨‍💻 Author

**Muneeb Fayaz**
Built with Python, Flask, and Ollama.

⭐ If you like this project, consider giving it a star!
