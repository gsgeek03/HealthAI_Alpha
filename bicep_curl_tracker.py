import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
import mediapipe as mp
from pose_detector import PoseDetector
from Form import Form

class BicepCurlTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Bicep Curl Tracking")
        self.root.geometry("1000x550")
        self.count = 0
        self.stage = "Fixed Form"
        self.detector = PoseDetector()
        self.cap = cv2.VideoCapture(0)
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        # Camera Frame
        self.camera_frame = ttk.Frame(self.root)
        self.camera_frame.pack(expand=True, fill="both")

        # Count Label inside Camera Frame
        self.count_label = ttk.Label(self.camera_frame, text="Count: 0", font=("Arial", 18))
        self.count_label.grid(row=0, column=2, pady=10,padx=10)

        # Status Label inside Camera Frame
        self.status_label = ttk.Label(self.camera_frame, text="Status: Fix Form", font=("Arial", 18))
        self.status_label.grid(row=1, column=2, pady=10,padx=10)

        # Exit Button
        exit_button = ttk.Button(self.camera_frame, text="Exit", command=self.exit_program)
        exit_button.grid(row=2, column=2, pady=10,padx=10)

        # Insights Button
        chatgpt_btn = ttk.Button(self.camera_frame, text="Insights", command=self.show_insights)
        chatgpt_btn.grid(row=3, column=2, pady=10,padx=10)
        self.create_widgets()

    def create_widgets(self):
        # Display camera feed
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

            angle, stage = self.calculate_angle(frame)

            if angle > 160:
                self.stage = "down"
            if angle < 30 and self.stage == "down":
                self.stage = "up"
                self.count += 1

            self.count_label.config(text=f"Count: {int(self.count)}")
            self.status_label.config(text=f"Status: {self.stage}")

        self.root.after(10, self.display_camera_feed)

    def calculate_angle(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                        landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                        landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                angle = self.calculate_angle_helper(shoulder, elbow, wrist)
                return angle, self.stage
            else:
                return 0, self.stage

        except Exception as e:
            print(e)
            return 0, self.stage

    @staticmethod
    def calculate_angle_helper(a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    def exit_program(self):
        self.cap.release()
        self.root.destroy()
    
    def show_insights(self):
        self.root.destroy()
        Form_window = tk.Tk() 
        Form(Form_window,"Bicep Curl",self.count, 0)
        if self.cap.isOpened():
            self.cap.release()
        Form_window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = BicepCurlTracker(root)
    root.mainloop() 