  JARVIS AI Assistant
<div align="center">

A voice-controlled AI assistant inspired by JARVIS from Iron Man, powered by Groq AI

Features • Installation • Usage • Commands • Contributing
</div>
✨ Features

     Continuous Voice Recognition - Always listening, just like the real JARVIS

     Natural Text-to-Speech - Cool, deep voice responses
     Groq AI Integration - Lightning-fast AI responses (100% FREE!)

     Text Mode - Press Ctrl+Alt+Space for a popup to type or speak

     Web Automation - Opens websites, searches Google, plays YouTube videos

     WhatsApp Quick Access - Instant WhatsApp Web opening

     Time & Date - Voice-activated time and date

     Smart Conversations - Powered by Llama 3.3 70B model

📋 Prerequisites

    Python 3.8 or higher
    Microphone
    Speakers/Headphones
    Internet connection
    Groq API key (FREE - no credit card required!)

 Installation
1. Clone the Repository
bash

git clone https://github.com/yourusername/jarvis-ai-assistant.git
cd jarvis-ai-assistant

2. Install Dependencies

Windows:
bash

pip install -r requirements.txt

macOS:
bash

pip install -r requirements.txt
brew install portaudio  # Required for PyAudio

Linux (Ubuntu/Debian):
bash

sudo apt-get install python3-pyaudio portaudio19-dev python3-tk
pip install -r requirements.txt

3. Install PyAudio (If pip install fails)

Windows:

    Download the appropriate .whl file from here
    Install: pip install PyAudio‑0.2.11‑cp311‑cp311‑win_amd64.whl

macOS:
bash

brew install portaudio
pip install pyaudio

Linux:
bash

sudo apt-get install python3-pyaudio

4. Get Your FREE Groq API Key

    Go to console.groq.com
    Sign up (100% FREE - no credit card needed!)
    Navigate to API Keys
    Click "Create API Key"
    Copy your key

5. Configure Environment

Create a .env file in the project root:
env

GROQ_API_KEY=your_groq_api_key_here

🎮 Usage
Start JARVIS
bash

python main.py

Two Modes of Operation
1. Voice Mode (Default)

    Just speak naturally after launching
    JARVIS listens continuously
    Say "goodbye" or "exit" to quit

2. Text Mode

    Press Ctrl+Alt+Space anywhere to open popup
    Type your command OR click "Use Voice"
    See responses in real-time

🎤 Voice Commands
Basic Commands

    "What time is it?" - Current time
    "What's the date?" - Current date
    "Exit" / "Goodbye" - Shut down JARVIS

Web Navigation

    "Open YouTube" - Opens YouTube
    "Open WhatsApp" - Opens WhatsApp Web
    "Open Google" - Opens Google
    "Open Gmail" - Opens Gmail
    "Open Facebook/Twitter/Instagram" - Social media sites
    "Open ChatGPT" - Opens ChatGPT website

Search & Play

    "Search for [query]" - Google search
    "Play [song/video] on YouTube" - YouTube search
    "Search [anything]" - Web search

AI Conversations

    Ask anything! Examples:
        "What's the weather like today?"
        "Tell me a joke"
        "Explain quantum physics"
        "Write a poem about AI"
        "Help me code a function in Python"

⚙️ Configuration

Edit main.py to customize:
python

# Speech rate (default: 175)
self.engine.setProperty('rate', 175)

# Volume (0.0 to 1.0)
self.engine.setProperty('volume', 1.0)

# Listening timeout (seconds)
audio = self.recognizer.listen(source, timeout=5)

# AI model (default: llama-3.3-70b-versatile)
model="llama-3.3-70b-versatile"

🔧 Troubleshooting
Microphone Not Working

    Verify microphone is connected and enabled
    Set as default device in system settings
    Try running with administrator privileges (Windows)

PyAudio Installation Issues

    Windows: Use .whl file from the link above
    macOS: brew install portaudio first
    Linux: Install system packages first

Hotkey Not Working

    Make sure no other app is using Ctrl+Alt+Space
    Run with sufficient permissions
    On Linux, you may need to run as sudo

API Errors

    Verify your API key in .env file
    Check internet connection
    Groq free tier limits: 30 requests/minute

No Voice/Audio Output

    Check speaker/headphone connections
    Verify system audio settings
    Try different TTS voice in code

 Why Groq?
Feature	Groq	ChatGPT	DeepSeek
Cost	🟢 FREE	🔴 $0.50+/M tokens	🟡 $0.14/M tokens
Speed	🟢 Ultra Fast	🟡 Fast	🟡 Fast
Model	Llama 3.3 70B	GPT-3.5/4	DeepSeek-Chat
Signup	No CC Required	CC Required	CC Required
Rate Limit	30/min free	Paid only	Paid only
  Project Structure

jarvis-ai-assistant/
│
├── main.py              # Main JARVIS application
├── requirements.txt     # Python dependencies
├── .env                 # API keys (create this)
├── .env.example         # Example env file
├── README.md           # This file
└── .gitignore          # Git ignore file

🤝 Contributing

Contributions are welcome! Here's how:

    Fork the repository
    Create your feature branch (git checkout -b feature/AmazingFeature)
    Commit your changes (git commit -m 'Add some AmazingFeature')
    Push to the branch (git push origin feature/AmazingFeature)
    Open a Pull Request

  Future Enhancements

    Send WhatsApp messages automatically
    Email integration
    Calendar management
    Smart home control
    File operations (create, read, delete)
    Weather integration
    News updates
    Spotify control
    System control (shutdown, restart, etc.)
    Memory persistence across sessions

📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

    Inspired by JARVIS from Iron Man
    Powered by Groq for lightning-fast AI
    Built with Python and love 

📧 Contact

Have questions? Feel free to reach out!

    GitHub: @yourusername
    Email: your.email@example.com

<div align="center">

⭐ Star this repo if you found it helpful!

Made with ❤️ by [Vihaan]
</div>
