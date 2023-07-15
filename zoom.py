import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
from PIL import Image
import os
import threading

class ZoomApp:
    def __init__(self, root):
        self.root = root
        root.title("Image Zoom-Out Video Generator")

        self.frame = tk.Frame(root, padx=10, pady=10)
        self.frame.pack()

        # Instructions
        tk.Label(self.frame, text="Please provide the following details to generate the video:", 
                 font=("Helvetica", 14)).grid(row=0, column=0, sticky="w", columnspan=2)

        # Image selection
        tk.Label(self.frame, text="Image File:", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w")
        self.image_path_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.image_path_var, width=50).grid(row=1, column=1)
        tk.Button(self.frame, text="Browse", command=self.browse_image).grid(row=1, column=2)

        # Video duration
        tk.Label(self.frame, text="Video Duration (sec):", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w")
        self.video_duration_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.video_duration_var).grid(row=2, column=1)

        # Frame rate
        tk.Label(self.frame, text="Frames per Second:", font=("Helvetica", 12)).grid(row=3, column=0, sticky="w")
        self.fps_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.fps_var).grid(row=3, column=1)

        # Output directory
        tk.Label(self.frame, text="Output Directory:", font=("Helvetica", 12)).grid(row=4, column=0, sticky="w")
        self.output_dir_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.output_dir_var, width=50).grid(row=4, column=1)
        tk.Button(self.frame, text="Browse", command=self.browse_directory).grid(row=4, column=2)
        
        # Dropdown menu for start position
        tk.Label(self.frame, text="Start Position:", font=("Helvetica", 12)).grid(row=5, column=0, sticky="w")
        self.start_position_var = tk.StringVar()
        self.start_position_combobox = ttk.Combobox(self.frame, textvariable=self.start_position_var)
        self.start_position_combobox['values'] = ('Top Left', 'Top Right', 'Bottom Left', 'Bottom Right', 'Center Top', 'Center Bottom', 'Center')
        self.start_position_combobox.grid(row=5, column=1)

        # Button to generate video
        self.button = tk.Button(self.frame, text="Generate Video", command=self.open_image, font=("Helvetica", 12), bg="blue", fg="white")
        self.button.grid(row=6, column=0, columnspan=3)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.frame, length=300, variable=self.progress_var)
        self.progress_bar.grid(row=8, column=0, columnspan=3)
        self.progress_bar.grid_remove()  # Hide progress bar initially

        # Status label
        self.label = tk.Label(self.frame, text="", font=("Helvetica", 12))
        self.label.grid(row=7, column=0, columnspan=3)

    def browse_image(self):
        # Open a file dialog and get the path of the selected image
        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.image_path_var.set(image_path)

    def browse_directory(self):
        # Open a directory dialog and get the path of the selected directory
        output_dir = filedialog.askdirectory()
        self.output_dir_var.set(output_dir)

    def open_image(self):
        self.button.config(state='disabled')  # Disable button during processing

        # Get the user inputs
        try:
            image_path = self.image_path_var.get()
            output_dir = self.output_dir_var.get()
            video_duration = float(self.video_duration_var.get())
            fps = int(self.fps_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for the video duration and frames per second.")
            self.button.config(state='normal')  # Enable button
            return

        # Check if a valid image path and output directory were provided
        if not image_path or not output_dir:
            messagebox.showinfo("Info", "Please select an image file and an output directory.")
            self.button.config(state='normal')  # Enable button
            return

        # Update label to show that processing has started
        self.label.config(text="Processing...")

        # Process image in a separate thread to avoid blocking the UI
        self.progress_var.set(0)  # Reset progress bar
        self.progress_bar.grid()  # Show progress bar
        thread = threading.Thread(target=self.process_image, args=(image_path, output_dir, video_duration, fps, self.progress_var))
        thread.start()

        # Start a periodic function that updates the progress bar
        self.update_progress_bar()

    def update_progress_bar(self):
        # Schedule this function to run again after 100 ms
        self.root.after(100, self.update_progress_bar)
        if self.progress_var.get() >= 100:
            self.progress_bar.grid_remove()

    def process_image(self, image_path, output_dir, video_duration, fps, progress_var):
        # Calculate the number of frames based on the duration
        num_frames_video = int(video_duration * fps)

        # Load the image
        img2 = Image.open(image_path)

        # Get start position from dropdown menu
        start_position = self.start_position_var.get()

        # Define the size of the initial zoomed-in area as a fraction of the image size
        fraction = 0.05
        crop_width = int(img2.width * fraction)
        crop_height = int(img2.height * fraction)

        # Set coordinates for the starting frame based on the selected start position
        if start_position == 'Top Left':
            left_start = 0
            upper_start = 0
        elif start_position == 'Top Right':
            left_start = img2.width - crop_width
            upper_start = 0
        elif start_position == 'Bottom Left':
            left_start = 0
            upper_start = img2.height - crop_height
        elif start_position == 'Bottom Right':
            left_start = img2.width - crop_width
            upper_start = img2.height - crop_height
        elif start_position == 'Center Top':
            left_start = (img2.width - crop_width) // 2
            upper_start = 0
        elif start_position == 'Center Bottom':
            left_start = (img2.width - crop_width) // 2
            upper_start = img2.height - crop_height
        elif start_position == 'Center':
            left_start = (img2.width - crop_width) // 2
            upper_start = (img2.height - crop_height) // 2

        # Generate frames for zoom effect
        frames_video = []
        for i in range(num_frames_video):
            # Calculate current crop box
            left = int(left_start * (1 - i / num_frames_video))
            upper = int(upper_start * (1 - i / num_frames_video))
            right = left + int(img2.width * (i / num_frames_video + fraction))
            lower = upper + int(img2.height * (i / num_frames_video + fraction))

            # Crop and resize image
            result = img2.crop((left, upper, right, lower)).resize(img2.size)
            frames_video.append(result)

            # Save frame as PNG
            frame_path = os.path.join(output_dir, f"frame_{i:04d}.png")
            result.save(frame_path)

            # Update progress var
            progress_var.set((i + 1) / num_frames_video * 100)

        # Create video
        frame_paths = [os.path.join(output_dir, f"frame_{i:04d}.png") for i in range(num_frames_video)]
        frame = cv2.imread(frame_paths[0])
        height, width, layers = frame.shape

        video_path = os.path.join(output_dir, "zoom_effect.mp4")
        video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

        for frame_path in frame_paths:
            video.write(cv2.imread(frame_path))

        cv2.destroyAllWindows()
        video.release()

        # Update label to show that processing is complete
        self.label.config(text="Processing complete!")

        # Re-enable button
        self.root.after(0, self.button.config, {'state': 'normal'})


root = tk.Tk()
app = ZoomApp(root)
root.mainloop()
