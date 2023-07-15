import tkinter as tk
from tkinter import filedialog, messagebox
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

        # Button to generate video
        self.button = tk.Button(self.frame, text="Generate Video", command=self.open_image, font=("Helvetica", 12), bg="blue", fg="white")
        self.button.grid(row=5, column=0, columnspan=3)

        # Status label
        self.label = tk.Label(self.frame, text="", font=("Helvetica", 12))
        self.label.grid(row=6, column=0, columnspan=3)

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
        thread = threading.Thread(target=self.process_image, args=(image_path, output_dir, video_duration, fps))
        thread.start()

    def process_image(self, image_path, output_dir, video_duration, fps):
        # Calculate the number of frames based on the duration
        num_frames_video = int(video_duration * fps)

        # Load the image
        img2 = Image.open(image_path)

        # Coordinates for the 640x384 region at the bottom center of the larger image
        left = (img2.width - 640) // 2
        upper = img2.height - 384
        right = left + 640
        lower = upper + 384

        # Crop the larger image to get the initial frame
        initial_frame = img2.crop((left, upper, right, lower))

        # Resize initial frame to be the same size as the larger one
        initial_frame_resized = initial_frame.resize(img2.size)

        # Define parameters for zoom effect
        step_sizes_video = np.linspace(0, 1, num_frames_video)

        # Generate frames for zoom effect
        frames_video = []
        for i, step in enumerate(step_sizes_video):
            # Linear interpolation between initial_frame_resized and img2
            result = Image.blend(initial_frame_resized, img2, step)
            frames_video.append(result)

            # Save frame as PNG
            frame_path = os.path.join(output_dir, f"frame_{i:04d}.png")
            result.save(frame_path)

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
