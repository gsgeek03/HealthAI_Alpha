import tkinter as tk
from tkinter import ttk, scrolledtext
import google.generativeai as genai # Import the generative AI module
import json



class BardPage:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.root.title("Insights")
        self.root.geometry("500x600")
        insights_text = self.fetch_insights()      
        scrolled_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=40, height=5, font=("Arial", 14))
        scrolled_text.insert(tk.END, insights_text)
        scrolled_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)     
        exit_button = ttk.Button(self.root, text="Exit", command=lambda: self.exit_program(self.root))
        exit_button.pack(pady=20)

    def fetch_insights(self):
        data=self.data
        genai.configure(api_key='AIzaSyCyo1cZCpSXwsrk6HqUGKHIDBU3BZuNc1U')
        model=genai.GenerativeModel('gemini-pro')
        data_json = json.dumps(data)
        response=model.generate_content(f"""System:  Given a user's workout data in JSON format, including their name, exercise duration, number of reps, and errors, generate personalized exercise tips and only one motivation quote. Give Proper Formatted response.
                                        User: {data_json}""")
        return response.text
    
    def exit_program(self, window=None):
        if window:
            window.destroy()
        else:
            self.root.destroy()
