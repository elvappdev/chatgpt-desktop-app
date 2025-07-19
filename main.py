import tkinter as tk
from tkinter import simpledialog, scrolledtext
import openai
import json
import os

CONFIG_FILE = "config.json"

# Check if API key exists or ask for it
def get_api_key():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            try:
                return json.load(f)['api_key']
            except (KeyError, json.JSONDecodeError):
                pass

    root.withdraw()
    api_key = simpledialog.askstring("API Key Required", "Enter your OpenAI API key:", show='*')
    if api_key:
        with open(CONFIG_FILE, 'w') as f:
            json.dump({'api_key': api_key}, f)
        return api_key
    else:
        root.destroy()
        exit()

# Send message to OpenAI
def send():
    user_input = entry.get()
    if not user_input.strip():
        return
    chat_history.insert(tk.END, "You: " + user_input + "\n")
    entry.delete(0, tk.END)
    root.update()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        reply = f"Error: {e}"

    chat_history.insert(tk.END, "GPT: " + reply + "\n\n")
    chat_history.yview(tk.END)

# Setup GUI
root = tk.Tk()
root.title("ChatGPT Desktop")

api_key = get_api_key()
openai.api_key = api_key

chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
chat_history.pack(padx=10, pady=10)

frame = tk.Frame(root)
entry = tk.Entry(frame, width=70)
entry.pack(side=tk.LEFT, padx=(0, 10))
send_button = tk.Button(frame, text="Send", command=send)
send_button.pack(side=tk.LEFT)
frame.pack(padx=10, pady=(0, 10))

entry.bind("<Return>", lambda event: send())
root.mainloop()
