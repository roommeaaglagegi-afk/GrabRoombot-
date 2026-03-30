from flask import Flask
from threading import Thread
import time
import asyncio
from importlib import import_module

# --- Highrise SDK Imports ---
from highrise import BaseBot
from highrise.__main__ import BotDefinition, main as highrise_main

# --- Flask Server (Bot ko zinda rakhne ke liye) ---
class WebServer():
    def __init__(self):
        self.app = Flask(__name__)
        @self.app.route('/')
        def index(): 
            return "Bot is Online and Running!"

    def run(self):
        self.app.run(host='0.0.0.0', port=5000)

    def keep_alive(self):
        t = Thread(target=self.run, daemon=True)
        t.start()

# --- Main Bot Runner ---
class RunBot():
    # Aapka Room ID aur Token
    room_id = "68e27f6e9796e3239f1cd493"
    bot_token = "f42d8a4ca6781a219ba6a75ea0cde26dc5229cfda5177554be6797b2a34b493b"
    
    def __init__(self):
        try:
            # Ye aapke 'main.py' se 'Bot' class ko load karega
            module = import_module("main")
            bot_instance = getattr(module, "Bot")()
            self.definitions = [BotDefinition(bot_instance, self.room_id, self.bot_token)]
            print("Bot definitions loaded successfully.")
        except Exception as e:
            print(f"Failed to load Bot from main.py: {e}")
            self.definitions = []

    def run_loop(self):
        if not self.definitions:
            print("No definitions found. Exiting...")
            return
        
        while True:
            try:
                print("Starting Highrise main loop...")
                asyncio.run(highrise_main(self.definitions))
            except Exception as e:
                print(f"Bot crashed with error: {e}. Restarting in 5 seconds...")
                time.sleep(5)

if __name__ == "__main__":
    # 1. Flask start karo
    server = WebServer()
    server.keep_alive()
    
    # 2. Bot start karo
    bot_runner = RunBot()
    bot_runner.run_loop()
