import tkinter as tk
from tkinter import ttk, scrolledtext
import openai
import json
import re
import google.generativeai as genai


class LLMFoodRecommendationPage:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.root.title("Food Recommendations")
        self.root.geometry("500x600")
        if(self.data["model"]=="chatgpt"):
            insights_text = self.fetch_insights()
        else:
            insights_text = self.fetch_insights_gemini()
        scrolled_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=40, height=5, font=("Arial", 14))
        scrolled_text.insert(tk.END, insights_text)
        scrolled_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        exit_button = ttk.Button(button_frame, text="Exit", command=lambda: self.exit_program(self.root))
        exit_button.grid(row=0, column=0, padx=10)

    def fetch_insights(self):
        data=self.data
        openai.api_key = "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"# Replace with your actual OpenAI API key
        data_json = json.dumps(data)
        user_message = {"role": "user", "content": data_json}
        messages = [
            {"role": "system", "content": f"""
            Given a user's data in JSON format, Recommend a indian food recipe for the user considering about his BMI and health. Give healthy recipes. Also give estimated nutrition value of the recipe.
            Also give warning to consult a doctor if facing any special disease condition. Also give warning that nutrional information is approximate and may vary according to the ingredients used.          
            """},
            {"role": "user", "content": data_json}
        ]
        response = self.get_completion(messages)
        return response

    def get_completion(self, messages, model="gpt-3.5-turbo"):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.9,  # this is the degree of randomness of the model's output 0-2
        )
        return response.choices[0].message["content"]
    
    def fetch_insights_gemini(self):
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
        response=model.generate_content(f"""System:  Given a user's data in JSON format, Recommend a indian food recipe for the user considering about his BMI and health. Give healthy recipes. Also give estimated nutrition value of the recipe.
            Also give warning to consult a doctor if facing any special disease condition. Also give warning that nutrional information is approximate and may vary according to the ingredients used.           
                                        User: {data_json}""")
        text=response.text
        formatted_response = re.sub(r'\*\*|\*|_', '', text)
        return formatted_response

