import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import subprocess
import sys

# Function to validate that the name contains only alphabets
def validate_name(char):
    return char.isalpha() or char == ""

# Function to validate that the ID contains only numerals
def validate_id(char):
    return char.isdigit() or char == ""

# Function to handle login and proceed to the object detection
def login():
    name = name_entry.get()
    id_number = id_entry.get()
    
    # Create a folder name using the name and ID
    folder_name = f"{name}_{id_number}"
    
    if name and id_number:
        # Check if the folder already exists
        if os.path.exists(folder_name):
            messagebox.showwarning("Login Failed", "This combination of Name and ID has already been used. Please use a different one.")
        else:
            # Create the folder
            os.makedirs(folder_name)
            
            # Save the name and ID in a text file within the folder
            with open(os.path.join(folder_name, "user_info.txt"), "w") as file:
                file.write(f"Name: {name}\nID: {id_number}\n")
            
            # Show success message and proceed
            messagebox.showinfo("Login Successful", f"Welcome, {name}!")
            root.destroy()  # Close the login window
            
            # Run the object detection script using the current Python interpreter
            script_path = os.path.join(os.getcwd(), 'object_detection.py')
            print("Script Path:", script_path)
            print("Python Executable:", sys.executable)
            
            try:
                # Use Popen to run the script
                result = subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Output any possible messages to the console for debugging
                stdout, stderr = result.communicate()
                print(stdout.decode('utf-8'))
                if stderr:
                    print(stderr.decode('utf-8'))
            except Exception as e:
                print("Error starting object detection:", e)
                messagebox.showerror("Error", f"Failed to start object detection: {e}")
    else:
        messagebox.showwarning("Login Failed", "Please enter both Name and ID.")

# Create main window for login
root = tk.Tk()
root.title("LESS (Learning about Environment Software System) - Login")

# Get screen dimensions for full-screen background
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

# Load and resize background image (JPG format) to full screen size
bg_image = Image.open("trees_login.jpg")  # Make sure the image is in the same directory or provide the full path.
bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)  # Resize the image to fit the screen
bg_image = ImageTk.PhotoImage(bg_image)

# Create a label to display the background image
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a frame for the login form with a slightly transparent background
form_frame = tk.Frame(root, bg="#ffffff", bd=0, highlightbackground="#000000", highlightthickness=1)
form_frame.place(relx=0.5, rely=0.5, anchor='center')

# Name label and entry box
name_label = tk.Label(form_frame, text="Name:", font=("Arial", 14), bg="#ffffff")
name_label.grid(row=0, column=0, pady=10, padx=5, sticky='w')

name_entry = tk.Entry(form_frame, font=("Arial", 14), bg="#f0f0f0", width=30, bd=2, relief="groove")
name_entry.grid(row=0, column=1, pady=10, padx=5)
name_entry.config(validate="key", validatecommand=(root.register(validate_name), '%S'))

# ID label and entry box
id_label = tk.Label(form_frame, text="ID:", font=("Arial", 14), bg="#ffffff")
id_label.grid(row=1, column=0, pady=10, padx=5, sticky='w')

id_entry = tk.Entry(form_frame, font=("Arial", 14), bg="#f0f0f0", width=30, bd=2, relief="groove")
id_entry.grid(row=1, column=1, pady=10, padx=5)
id_entry.config(validate="key", validatecommand=(root.register(validate_id), '%S'))

# Login button
login_button = tk.Button(form_frame, text="Login", font=("Arial", 14), bg="#007BFF", fg="#ffffff", command=login)
login_button.grid(row=2, columnspan=2, pady=20)

root.mainloop()
