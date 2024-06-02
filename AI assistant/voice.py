import tkinter as tk
import pyttsx3

def text_to_speech():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    selected_voice = var.get()
    for voice in voices:
        if voice.name == selected_voice:
            engine.setProperty('voice', voice.id)
            break
    engine.say(entry.get())
    engine.runAndWait()

root = tk.Tk()
root.title("Text to Speech")

var = tk.StringVar(value="")
voices = pyttsx3.init().getProperty('voices')
options = [voice.name for voice in voices]
option_menu = tk.OptionMenu(root, var, *options)
option_menu.pack()

entry_label = tk.Label(root, text="Enter text:")
entry_label.pack()
entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Speak", command=text_to_speech)
button.pack()

root.mainloop()
