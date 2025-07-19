import tkinter as tk
from tkinter import simpledialog, scrolledtext
import openai
import json
import os

CONFIG_FILE = "config.json"

# Setup GUI early for prompt to work
root = tk.Tk()
root.withdraw()  # Hide the main window until you receive the key

# get key
def get_api_key():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                if 'api_key' in data and data['api_key'].startswith('sk-'):
                    return data['api_key']
        except (json.JSONDecodeError, KeyError):
            pass

    # Если ключ не найден — спрашиваем пользователя
    api_key = simpledialog.askstring("OpenAI API Key", "Enter your OpenAI API key:", show='*')
    if api_key:
        with open(CONFIG_FILE, 'w') as f:
            json.dump({'api_key': api_key}, f)
        return api_key
    else:
        tk.messagebox.showerror("Error", "API key is required to continue.")
        root.destroy()
        exit()

# Sending a message
def send():
    user_input = entry.get()
    if not user_input.strip():
        return
    chat_history.insert(tk.END, "You: " + user_input + "\n")
    entry.delete(0, tk.END)
    root.update()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or gpt-4 if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        reply = f"GPT: Error: {e}"

    chat_history.insert(tk.END, reply + "\n\n")
    chat_history.yview(tk.END)

# Запускаем GUI
api_key = get_api_key()
openai.api_key = api_key

root.deiconify()  # Show the main window

root.title("ChatGPT Desktop")
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

