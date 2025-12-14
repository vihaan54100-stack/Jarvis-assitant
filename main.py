import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
import threading
import tkinter as tk
from tkinter import ttk
from pynput import keyboard

try:
    from groq import Groq
    from dotenv import load_dotenv
    load_dotenv()
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("Warning: groq or dotenv not installed. AI features will be limited.")

class JARVIS:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 175)  # Slightly faster for cool effect
        self.engine.setProperty('volume', 1.0)
        
        # Set a cool deep voice
        voices = self.engine.getProperty('voices')
        for voice in voices:
            # Try to find David or other male voices
            if any(name in voice.name.lower() for name in ['david', 'male', 'zira']) and 'female' not in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        
        # Initialize Groq AI
        if AI_AVAILABLE:
            api_key = os.getenv('GROQ_API_KEY')
            if api_key:
                self.client = Groq(api_key=api_key)
            else:
                self.client = None
                print("Groq API key not found in .env file")
        else:
            self.client = None
        
        # Conversation history for context
        self.conversation_history = []
        
        # Continuous listening flag
        self.is_listening = True
        self.is_active = True
        
        # Text mode popup
        self.text_popup = None
        
        # Setup hotkey listener
        self.setup_hotkey()
        
        print("JARVIS initialized successfully!")
    
    def setup_hotkey(self):
        """Setup Ctrl+Alt+Space hotkey"""
        def on_activate():
            self.show_text_popup()
        
        # Define the hotkey combination
        hotkey = keyboard.HotKey(
            keyboard.HotKey.parse('<ctrl>+<alt>+<space>'),
            on_activate
        )
        
        def for_canonical(f):
            return lambda k: f(keyboard_listener.canonical(k))
        
        keyboard_listener = keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release)
        )
        keyboard_listener.start()
    
    def show_text_popup(self):
        """Show text input popup"""
        if self.text_popup and self.text_popup.winfo_exists():
            self.text_popup.lift()
            return
        
        self.text_popup = tk.Tk()
        self.text_popup.title("JARVIS - Text Mode")
        self.text_popup.geometry("600x400")
        self.text_popup.configure(bg='#1a1a1a')
        
        # Title
        title = tk.Label(
            self.text_popup,
            text="🤖 JARVIS Text Interface",
            font=('Arial', 16, 'bold'),
            bg='#1a1a1a',
            fg='#00d4ff'
        )
        title.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(self.text_popup, bg='#1a1a1a')
        input_frame.pack(pady=10, padx=20, fill='x')
        
        # Text entry
        self.text_entry = tk.Text(
            input_frame,
            height=3,
            font=('Arial', 12),
            bg='#2a2a2a',
            fg='white',
            insertbackground='white',
            relief='flat',
            padx=10,
            pady=10
        )
        self.text_entry.pack(fill='x', pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(self.text_popup, bg='#1a1a1a')
        btn_frame.pack(pady=10)
        
        # Send button
        send_btn = tk.Button(
            btn_frame,
            text="📤 Send Text",
            command=self.process_text_input,
            font=('Arial', 11, 'bold'),
            bg='#00d4ff',
            fg='black',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        send_btn.pack(side='left', padx=5)
        
        # Voice button
        voice_btn = tk.Button(
            btn_frame,
            text="🎤 Use Voice",
            command=self.process_voice_from_popup,
            font=('Arial', 11, 'bold'),
            bg='#ff6b00',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        voice_btn.pack(side='left', padx=5)
        
        # Response area
        response_label = tk.Label(
            self.text_popup,
            text="Response:",
            font=('Arial', 12, 'bold'),
            bg='#1a1a1a',
            fg='#00d4ff'
        )
        response_label.pack(pady=(10, 5))
        
        self.response_text = tk.Text(
            self.text_popup,
            height=8,
            font=('Arial', 11),
            bg='#2a2a2a',
            fg='white',
            relief='flat',
            padx=10,
            pady=10,
            state='disabled'
        )
        self.response_text.pack(padx=20, fill='both', expand=True)
        
        # Bind Enter key
        self.text_entry.bind('<Return>', lambda e: self.process_text_input())
        
        # Focus on text entry
        self.text_entry.focus()
        
        self.text_popup.mainloop()
    
    def process_text_input(self):
        """Process text input from popup"""
        command = self.text_entry.get('1.0', 'end-1c').strip()
        if command:
            self.text_entry.delete('1.0', 'end')
            self.update_response(f"You: {command}\n\n")
            
            # Process command
            response = self.process_command_text(command)
            self.update_response(f"JARVIS: {response}\n")
            self.speak(response)
    
    def process_voice_from_popup(self):
        """Process voice input from popup"""
        self.update_response("🎤 Listening...\n")
        command = self.listen()
        if command:
            self.update_response(f"You: {command}\n\n")
            response = self.process_command_text(command)
            self.update_response(f"JARVIS: {response}\n")
            self.speak(response)
    
    def update_response(self, text):
        """Update response text area"""
        if self.text_popup and self.text_popup.winfo_exists():
            self.response_text.config(state='normal')
            self.response_text.insert('end', text)
            self.response_text.see('end')
            self.response_text.config(state='disabled')
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"JARVIS: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen to user's voice command"""
        with sr.Microphone() as source:
            print("\n🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                command = self.recognizer.recognize_google(audio)
                print(f"You: {command}")
                return command.lower()
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                self.speak("Speech recognition service is unavailable.")
                return ""
    
    def chat_ai(self, prompt):
        """Get response from Groq AI"""
        if not AI_AVAILABLE:
            return "AI is not available. Please install: pip install groq python-dotenv"
        
        if not self.client:
            return "Groq API key not found. Please add it to the .env file. It's completely FREE!"
        
        try:
            self.conversation_history.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=self.conversation_history,
                max_tokens=200,
                temperature=0.8
            )
            
            reply = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": reply})
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return reply
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "authentication" in error_msg.lower():
                return "Invalid API key. Please check your .env file and get a free key from console.groq.com"
            else:
                return f"I'm having trouble connecting to my AI brain. Error: {error_msg}"
    
    def open_website(self, url):
        """Open a website in the default browser"""
        webbrowser.open(url)
        return f"Opening {url}"
    
    def search_web(self, query):
        """Search the web using Google"""
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        return f"Searching for {query}"
    
    def open_youtube(self, query=None):
        """Open YouTube or search for a video"""
        if query:
            search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return f"Searching YouTube for {query}"
        else:
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube"
    
    def open_whatsapp(self):
        """Open WhatsApp Web"""
        webbrowser.open("https://web.whatsapp.com")
        return "Opening WhatsApp Web"
    
    def tell_time(self):
        """Tell the current time"""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The time is {time_str}"
    
    def tell_date(self):
        """Tell the current date"""
        now = datetime.datetime.now()
        date_str = now.strftime("%B %d, %Y")
        return f"Today is {date_str}"
    
    def process_command_text(self, command):
        """Process command and return text response"""
        if not command:
            return ""
        
        # Exit commands
        if any(word in command for word in ['exit', 'quit', 'goodbye', 'bye']):
            self.is_active = False
            return "Goodbye sir. It has been a pleasure serving you. Until next time!"
        
        # Time and date
        elif 'time' in command:
            return self.tell_time()
        
        elif 'date' in command:
            return self.tell_date()
        
        # Open websites
        elif 'open youtube' in command:
            query = command.replace('open youtube', '').strip()
            return self.open_youtube(query if query else None)
        
        elif 'open whatsapp' in command:
            return self.open_whatsapp()
        
        elif 'open chatgpt' in command or 'open chat gpt' in command:
            return self.open_website("https://chat.openai.com")
        
        elif 'open' in command and any(word in command for word in ['google', 'gmail', 'facebook', 'twitter', 'instagram']):
            if 'google' in command:
                return self.open_website("https://www.google.com")
            elif 'gmail' in command:
                return self.open_website("https://mail.google.com")
            elif 'facebook' in command:
                return self.open_website("https://www.facebook.com")
            elif 'twitter' in command:
                return self.open_website("https://www.twitter.com")
            elif 'instagram' in command:
                return self.open_website("https://www.instagram.com")
        
        # Search commands
        elif 'search for' in command or 'search' in command:
            query = command.replace('search for', '').replace('search', '').strip()
            if query:
                return self.search_web(query)
        
        # YouTube search
        elif 'play' in command and 'youtube' in command:
            query = command.replace('play', '').replace('on youtube', '').replace('youtube', '').strip()
            return self.open_youtube(query)
        
        # AI conversation
        else:
            return self.chat_ai(command)
    
    def process_command(self, command):
        """Process user commands (voice mode)"""
        if not command:
            return True
        
        response = self.process_command_text(command)
        if response:
            self.speak(response)
        
        return self.is_active
    
    def run(self):
        """Main run loop with continuous listening"""
        self.speak("JARVIS online and ready for continuous operation, sir. Press Control Alt Space for text mode, or just speak naturally. I'm always listening.")
        
        while self.is_active:
            command = self.listen()
            if command and not self.process_command(command):
                break
        
        print("\nJARVIS shutting down...")

if __name__ == "__main__":
    jarvis = JARVIS()
    jarvis.run()