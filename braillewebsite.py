import tkinter as tk
from tkinter import Text, Scrollbar
from googletrans import Translator
from gtts import gTTS
import os

class BrailleTranslatorApp:
    def _init_(self, root):
        self.root = root
        self.root.title("TRANSVOX-Braille Translator")
        self.translator = Translator()

       
        self.create_braille_keyboard()

        self.create_braille_input_area()

       
        self.create_translation_result_area()
        self.center_window()
        self.setup_style()
    def setup_style(self):
        self.root.configure(bg='#f0f0f0')
        self.default_font=("Arial",12)
        self.heading_font=("Arial",16,"bold")
        
    def create_braille_keyboard(self):
        braille_keys = [
        ('a','⠁'), ('b','⠃'), ('c','⠉'), ('d','⠙'), ('e','⠑'),
        ('f','⠋'), ('g','⠛'), ('h','⠓'), ('i','⠊'), ('j','⠚'),
        ('k','⠅'), ('l','⠇'), ('m','⠍'), ('n','⠝'), ('o','⠕'),
        ('p','⠏'), ('q','⠟'), ('r','⠗'), ('s','⠎'), ('t','⠞'),
        ('u','⠥'), ('v','⠧'), ('w','⠺'), ('x','⠭'), ('y','⠽'),
        ('z','⠵'), (' ', ' ')
         ]

        keyboard_frame = tk.Frame(self.root,bg='#ffffff')
        keyboard_frame.place(relx=0.5,rely=0.25,anchor='center')
        tranvox_label=tk.Label(self.root,text='TRANVOX-Braille Translator',font=("helvetica",25))
        tranvox_label.place(relx=0.5,rely=0.09,anchor='center')
       
        
        

        for i, (braille, alphabet) in enumerate(braille_keys):
            btn = tk.Button(keyboard_frame, text=braille + '\n' + alphabet, width=3, height=2, command=lambda a=alphabet: self.insert_braille_char(a))
            btn.grid(row=i // 10, column=i % 10, padx=2, pady=2)
    def create_braille_input_area(self):
        input_frame = tk.Frame(self.root,bg='#ffffff')
        input_frame.place(relx=0.5,rely=0.5,anchor="center")
        

        input_label = tk.Label(input_frame, text="Braille Input:")
        input_label.grid(row=0, column=0, sticky='w')

        self.braille_text = Text(input_frame, height=5, width=50, wrap='word')
        self.braille_text.grid(row=1, column=0, pady=5,sticky='nsew')

        translate_button = tk.Button(input_frame, text="Translate", command=self.translate_and_speak)
        translate_button.grid(row=2, column=0, pady=5)

        clear_button=tk.Button(input_frame,text="Clear",command=self.clear_braille_input)
        clear_button.grid(row=3,column=0,pady=6)

    def clear_braille_input(self):
        self.braille_text.delete('1.0',tk.END)

    def create_translation_result_area(self):
        result_frame = tk.Frame(self.root,bg='#ffffff')
        
        result_frame.place(relx=0.5,rely=0.75,anchor='center')

        result_label = tk.Label(result_frame, text="Translation Result:")
        result_label.grid(row=0, column=0, sticky='w')
        

        self.result_text = Text(result_frame, height=5, width=50, wrap='word', state='disabled')
        self.result_text.grid(row=1, column=0, pady=5,sticky='nsew')

        

    def insert_braille_char(self, char):
        self.braille_text.insert(tk.END, char)

    def translate_and_speak(self):
        braille_text = self.braille_text.get("1.0", tk.END).strip()
        english_text = self.braille_to_english(braille_text)
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, english_text)
        self.result_text.config(state='disabled')

        
        translate_and_speak(english_text)

    def braille_to_english(self, braille_text):
         braille_alphabet = {
        'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
        'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
        'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
        'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
        'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽',
        'z': '⠵', ' ': ' ',
        '1': '⠼⠁', '2': '⠼⠃', '3': '⠼⠉', '4': '⠼⠙', '5': '⠼⠑',
        '6': '⠼⠋', '7': '⠼⠛', '8': '⠼⠓', '9': '⠼⠊', '0': '⠼⠚'
        }
    
    
         english_text = ''
         current_word = ''
         for char in braille_text:
            if char in braille_alphabet.values():
                for key, value in braille_alphabet.items():
                    if char == value:
                        current_word += key
                        break
            elif char == ' ':  
                if current_word:
                     english_text += current_word + ' '
                     current_word = ''
            elif char == '⠼': 
                 continue 
            elif char == '\n':  
                 if current_word: 
                    english_text += current_word + '\n'
                    current_word = ''
            else:
         
                continue
    
         if current_word:
            english_text += current_word
    
         return english_text

        
    def center_window(self):
         screen_width=self.root.winfo_screenwidth()
         screen_height=self.root.winfo_screenheight()
         window_width=600
         window_height=400
         x_coordinate=(screen_width-window_width)//2
         y_coordinate=(screen_height-window_height)//2
         self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

def translate_and_speak(text, target_language='ml'):
    translator = Translator()

  
    translated_text = translator.translate(text, dest=target_language).text

    
    speech = gTTS(translated_text, lang=target_language)

    speech.save("translated_speech.mp3")

    
    os.system("start translated_speech.mp3")


if __name__ == "__main__":
    root = tk.Tk()
    app = BrailleTranslatorApp(root)
    root.mainloop()