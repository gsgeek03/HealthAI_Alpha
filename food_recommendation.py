import tkinter as tk
from tkinter import ttk
from LLM_Food_Recommendation import LLMFoodRecommendationPage

class MealSelectorApp:
    def __init__(self,root,data):
        self.root = root
        self.root.title("Meal Selector")
        self.root.geometry("450x350")

        self.veg_non_veg_var = tk.StringVar()
        self.egg_var = tk.StringVar()
        self.meal_type_var = tk.StringVar()
        self.data=data
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(expand=True, fill="both")

        # Create a dictionary to store radio button groups
        radio_groups = {
            "Vegetarian/Non-vegetarian": ["Vegetarian", "Non-vegetarian"],
            "Include/Exclude Egg": ["Include Egg", "Exclude Egg"],
            "Meal Type": ["Breakfast", "Lunch", "Quick Snack", "Dinner"]
        }

        # Create and place radio buttons dynamically
        self.place_radios(main_frame, radio_groups)

        # Submit Button
        ttk.Button(main_frame, text="Submit", command=self.submit).grid(row=len(radio_groups)*2, column=0, pady=20)
        ttk.Button(main_frame, text="Exit", command=self.exit_program).grid(row=len(radio_groups)*2, column=1, pady=20)

    def place_radios(self, frame, radio_groups):
        for i, (label, options) in enumerate(radio_groups.items()):
            ttk.Label(frame, text=label).grid(row=i*2, column=0, columnspan=len(options), sticky="w", pady=5)

            for j, option in enumerate(options):
                ttk.Radiobutton(frame, text=option, variable=self.get_variable(label), value=option).grid(row=i*2+1, column=j, padx=5, pady=5, sticky="w")

    def get_variable(self, label):
        if label == "Vegetarian/Non-vegetarian":
            return self.veg_non_veg_var
        elif label == "Include/Exclude Egg":
            return self.egg_var
        elif label == "Meal Type":
            return self.meal_type_var

    def submit(self):
        custom_data = {}
        custom_data["Name"] = self.data["name"]
        custom_data["Age"] = self.data["age"]
        custom_data["bmi"] = self.data["bmi"]
        custom_data["Vegetarian/Non-vegetarian"] = self.veg_non_veg_var.get()
        custom_data["Include/Exclude Egg"] = self.egg_var.get()
        custom_data["Meal Type"] = self.meal_type_var.get()
        custom_data["model"]=self.data["model"]
        self.root.destroy()
        food_recommendation_window = tk.Tk()
        LLMFoodRecommendationPage(food_recommendation_window, custom_data)
        food_recommendation_window.mainloop()
    
    def exit_program(self):
        self.root.destroy()

