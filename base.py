import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image
import os

def open_image():
    # Open a file dialog and get the path of the selected image
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    
    # Check if a valid image path was returned
    if not image_path:
        print("No image file selected.")
        return  # Exit the function if no image file was selected
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
    num_frames_video = 60  # Number of frames in the zoom effect
    fps = 10  # Frames per second for video
    step_sizes_video = np.linspace(0, 1, num_frames_video)

    # Generate frames for zoom effect
    frames_video = []
    for i, step in enumerate(step_sizes_video):
        # Linear interpolation between initial_frame_resized and img2
        result = Image.blend(initial_frame_resized, img2, step)
        frames_video.append(result)

        # Save frame as PNG
        result.save(f"frame_{i:04d}.png")

    # Create video
    frame_paths = [f"frame_{i:04d}.png" for i in range(num_frames_video)]
    frame = cv2.imread(frame_paths[0])
    height, width, layers = frame.shape

    video_path = "zoom_effect.mp4"
    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

    for frame_path in frame_paths:
        video.write(cv2.imread(frame_path))

    cv2.destroyAllWindows()
    video.release()

root = tk.Tk()

# Create a button that will call the open_image function when clicked
open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack()

root.mainloop()
