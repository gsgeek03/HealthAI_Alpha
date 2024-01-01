import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import cv2
from pose_detector import PoseDetector
from Form import Form

class Squat:
    def __init__(self, root):
        self.root = root
        self.root.title("Squat")
        self.root.geometry("1000x550")
        self.count = 0
        self.feedback = "Fix Form"
        self.detector = PoseDetector()
        self.cap = cv2.VideoCapture(0)
        self.error = 0
        self.direction = 0
        self.form = 0
        

        # Camera Frame
        self.camera_frame = ttk.Frame(self.root)
        self.camera_frame.pack(expand=True, fill="both")

        # Count Label inside Camera Frame
        self.count_label = ttk.Label(self.camera_frame, text="Count: 0", font=("Arial", 18))
        self.count_label.grid(row=0, column=2, pady=10,padx=10)

        # Status Label inside Camera Frame
        self.status_label = ttk.Label(self.camera_frame, text="Status: Do Squat", font=("Arial", 18))
        self.status_label.grid(row=1, column=2, pady=10,padx=10)

        # Exit Button
        exit_button = ttk.Button(self.camera_frame, text="Exit", command=self.exit_program)
        exit_button.grid(row=2, column=2, pady=10,padx=10)

        # Insights Button
        chatgpt_btn = ttk.Button(self.camera_frame, text="Insights", command=self.show_insights)
        chatgpt_btn.grid(row=3, column=2, pady=10,padx=10)

        bard_btn = ttk.Button(self.camera_frame, text="Insights", command=self.show_insights)
        bard_btn.grid(row=3, column=3, pady=10,padx=10)

        self.create_widgets()

    def create_widgets(self):
        self.display_camera_feed()

    def display_camera_feed(self):
        _, frame = self.cap.read()

        if frame is not None:
            frame, results = self.detector.find_pose(frame)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
            camera_label = ttk.Label(self.camera_frame, image=photo)
            camera_label.photo = photo
            camera_label.grid(row=0, column=1, rowspan=4)

            if results.pose_landmarks:
                lm_list = self.detector.find_position(frame, [], results)
                right_leg = self.detector.find_angle(frame, lm_list, 24, 26, 28, results, draw=False)
                left_leg = self.detector.find_angle(frame, lm_list, 23, 25, 27, results, draw=False)

                if right_leg >= 150 and left_leg >= 150:
                    self.form = 1

                if self.form == 1:
                        if right_leg >= 160 and left_leg >= 160:
                            self.feedback = "Do Squat"
                        elif right_leg < 80 and left_leg < 80:
                            self.error += 1
                            self.form = 0
                        elif right_leg >= 80 and right_leg<=100 and left_leg >= 80 and left_leg<=100:
                            self.feedback = "Correct Form. Keep Going"
                            self.count += 1
                            self.form = 0
                else:
                    self.form = 0
                # Update labels
                self.count_label.config(text=f"Count: {int(self.count)}")
                self.status_label.config(text=f"Status: {self.feedback}")

        self.root.after(10, self.display_camera_feed)

    def exit_program(self):
        self.cap.release()
        self.root.destroy()

    def show_insights(self):
        self.root.destroy()
        Form_window = tk.Tk() 
        Form(Form_window,"Squat",self.count, self.error)
        self.cap.release()
        Form_window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Squat(root)
    root.mainloop()        

