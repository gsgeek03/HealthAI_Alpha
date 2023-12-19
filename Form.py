import tkinter as tk
from tkinter import ttk
from insights_page import InsightsPage

class Form:
    def __init__(self, root, exercise, count, error):
        self.root = root
        self.root.title("User Information")
        self.root.geometry("700x300")
        self.exercise=exercise
        self.count=count
        self.error=error

        # Create labels
        name_label = ttk.Label(self.root, text="Name:")
        age_label = ttk.Label(self.root, text="Age:")
        weight_label = ttk.Label(self.root, text="Weight(in kgs):")
        height_label = ttk.Label(self.root, text="Height:")
        feet_label = ttk.Label(self.root, text="Feet:")
        inches_label = ttk.Label(self.root, text="Inches:")

        # Create entry fields
        self.name_entry = ttk.Entry(self.root)
        self.age_entry = ttk.Entry(self.root)
        self.weight_entry = ttk.Entry(self.root)
        self.feet_entry = ttk.Entry(self.root)
        self.inches_entry = ttk.Entry(self.root)

        # Position labels and entry fields
        name_label.grid(row=0, column=0, padx=10, pady=10)
        age_label.grid(row=1, column=0, padx=10, pady=10)
        weight_label.grid(row=2, column=0, padx=10, pady=10)
        height_label.grid(row=3, column=0, padx=2, pady=2)
        feet_label.grid(row=3, column=1, padx=2, pady=2)
        inches_label.grid(row=3, column=3, padx=2, pady=2)

        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.age_entry.grid(row=1, column=1, padx=10, pady=10)
        self.weight_entry.grid(row=2, column=1, padx=10, pady=10)
        self.feet_entry.grid(row=3, column=2, padx=2, pady=2)
        self.inches_entry.grid(row=3, column=4, padx=2, pady=2)

        # Create buttons
        exit_button = ttk.Button(self.root, text="Exit", command=self.exit_program)
        insights_button = ttk.Button(self.root, text="Insights", command=self.pass_data_to_insights)

        # Position buttons
        exit_button.grid(row=4, column=0, padx=10, pady=10)
        insights_button.grid(row=4, column=1, padx=10, pady=10)

    def exit_program(self):
        self.root.destroy()

    def pass_data_to_insights(self):
        data={
            'name': self.name_entry.get(),
            'age': self.age_entry.get(),
            'weight': self.weight_entry.get(),
            'feet': self.feet_entry.get(),
            'inches': self.inches_entry.get(),
            'exercise': self.exercise,
            'count': self.count,
            'error': self.error
        }
        self.root.destroy()
        insights_window = tk.Tk() 
        # Create an instance of the InsightsPage class and pass the data
        InsightsPage(insights_window, data)
        insights_window.mainloop()
        