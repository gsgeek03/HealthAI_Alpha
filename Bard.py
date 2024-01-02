import tkinter as tk
from tkinter import ttk, scrolledtext
import google.generativeai as genai # Import the generative AI module
import json
import re
from food_recommendation import MealSelectorApp

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
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        exit_button = ttk.Button(button_frame, text="Exit", command=lambda: self.exit_program(self.root))
        exit_button.grid(row=0, column=0, padx=10)
        food_button = ttk.Button(button_frame, text="Food Recommendation", command=self.show_food_page)
        food_button.grid(row=0, column=1, padx=10)

    def fetch_insights(self):
        data=self.data
        generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        }
        genai.configure(api_key='AIzaSyCyo1cZCpSXwsrk6HqUGKHIDBU3BZuNc1U')
        model=genai.GenerativeModel('gemini-pro', generation_config=generation_config)
        data_json = json.dumps(data)
        response=model.generate_content(f"""System:  Given a user's workout data in JSON format,
            including their name, exercise duration, number of reps, and errors, generate personalized exercise tips and only one motivation quote.
            Don't forget to mention about exercise type, BMI and BMI category. Don't mention about height, weight, error, count, duration etc.
            Include tips regarding weight too. Answer should be in proper format.        
                                        User: {data_json}""")
        text=response.text
        formatted_response = re.sub(r'\*\*|\*|_', '', text)
        return formatted_response
    
    def show_food_page(self):
        self.data["model"]="gemini"
        self.root.destroy()
        meal_selector_window = tk.Tk()
        MealSelectorApp(meal_selector_window,data=self.data)
        meal_selector_window.mainloop()
        

    def exit_program(self, window=None):
        if window:
            window.destroy()
        else:
            self.root.destroy()
