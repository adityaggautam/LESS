from tkinter import *
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import os
import time  # Importing time module
import partial_object_matching
import texture_and_shape
import edge_detection
import colour_recog  # Custom color recognition algorithm

# Function to calculate object speed (in km/h)
def calculate_speed(start_point, end_point, time_elapsed):
    distance = np.linalg.norm(np.array(end_point) - np.array(start_point))  # Pixel distance
    distance_in_meters = distance * 0.05  # Adjust this scale as per your use case
    speed_mps = distance_in_meters / time_elapsed  # Speed in meters per second
    speed_kmph = speed_mps * 3.6  # Convert to km/h
    return speed_kmph

# Function to detect the dominant color in an object
def get_dominant_color(image, roi):
    x, y, w, h = roi
    roi_img = image[y:y + h, x:x + w]
    average_color = np.mean(roi_img, axis=(0, 1))
    return average_color

# Function to handle object detection
def start_object_detection(video_source):
    print("Starting object detection...")
    cap = cv2.VideoCapture(video_source)  # Video source can be webcam or file path

    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}")
        return

    previous_positions = {}
    previous_times = {}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 150)

        # Apply custom edge detection algorithm
        edges = edge_detection.detect_edges(frame)

        # Find contours based on edges
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print(f"Contours detected: {len(contours)}")  # Debugging information

        for idx, contour in enumerate(contours):
            if cv2.contourArea(contour) > 500:  # Filter out small contours
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Calculate the speed of the object
                current_time = time.time()
                current_position = (x + w // 2, y + h // 2)
                
                if idx in previous_positions:
                    previous_position = previous_positions[idx]
                    time_elapsed = current_time - previous_times[idx]
                    speed = calculate_speed(previous_position, current_position, time_elapsed)
                    cv2.putText(frame, f"Speed: {speed:.2f} km/h", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                
                previous_positions[idx] = current_position
                previous_times[idx] = current_time

                # Detect the dominant color of the object
                dominant_color = get_dominant_color(frame, (x, y, w, h))
                color_text = f"Color: R={int(dominant_color[2])}, G={int(dominant_color[1])}, B={int(dominant_color[0])}"
                cv2.putText(frame, color_text, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                # Detect object color using advanced algorithm
                color_name = colour_recog.detect_color_name(dominant_color)
                cv2.putText(frame, f"Detected Color: {color_name}", (x, y + h + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

                # Apply partial object matching
                is_partial_match = partial_object_matching.match_partial_object(frame, (x, y, w, h))
                if is_partial_match:
                    cv2.putText(frame, "Partial Match Detected", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                # Apply texture and shape matching
                texture_shape_detected = texture_and_shape.detect_texture_shape(frame, (x, y, w, h))
                if texture_shape_detected:
                    cv2.putText(frame, "Texture & Shape Match", (x, y + h + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("Object Detection", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Login Function
def login_function(video_source=None):
    user_name = name_entry.get()  # Retrieve input from the username field
    user_id = id_entry.get()  # Retrieve input from the ID field
    if user_name and user_id:
        # Create a folder named "Name_ID" to save data locally
        folder_name = f"{user_name}_{user_id}"
        if os.path.exists(folder_name):
            response = messagebox.askyesno("Folder Exists", f"Folder '{folder_name}' already exists. Overwrite?")
            if response:
                print(f"Using existing folder '{folder_name}' and overwriting data.")
                start_object_detection(video_source)  # Start object detection
            else:
                print("Please choose a different ID.")
        else:
            os.makedirs(folder_name)
            print(f"Folder '{folder_name}' created.")
            start_object_detection(video_source)  # Start object detection after successful login
    else:
        print("Please enter both Name and ID.")

# Function to select a video file
def select_video_file():
    video_file_path = filedialog.askopenfilename(title="Select a Video File", filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))
    if video_file_path:
        login_function(video_source=video_file_path)  # Use the selected video file for detection

# Function to start live video detection
def start_live_video():
    login_function(video_source=0)  # Use webcam (0) for live video detection

# GUI for Login and Video Selection
root = Tk()
root.title("Login Page")
root.geometry("500x400")  # Adjusted the window size

# Username label and entry
name_label = Label(root, text="Name")
name_label.pack(pady=5)
name_entry = Entry(root)
name_entry.pack(pady=5)

# ID label and entry
id_label = Label(root, text="ID")
id_label.pack(pady=5)
id_entry = Entry(root)
id_entry.pack(pady=5)

# Button to start live video detection
live_button = Button(root, text="Use Live Video", command=start_live_video)
live_button.pack(pady=10)

# Button to select a video file for detection
video_button = Button(root, text="Select Video File", command=select_video_file)
video_button.pack(pady=10)

# Exit handling
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
