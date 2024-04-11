# composite-image
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:59:23 2024

@author: tgilmore10 (with ChatGPT)
"""
from tkinter import Tk, filedialog, messagebox
from PIL import Image
import os

def select_folder():
    root = Tk()
    root.withdraw()  # Hide the main window

    folder_path = filedialog.askdirectory()
    root.destroy()  # Close the tkinter window
    
    # Hard-coded this because tkinter was having issues on my desktop computer in Hardin
#    folder_path = "C:/Users/tgilmore10/OneDrive - University of Nebraska-Lincoln/RESEARCH PROJECTS/2021_GRIME_AI/temp PBT image subsets/Micks Slide Midday\MICKS SLIDE_13_to_15"
    print(folder_path)
    return folder_path

def crop_side(image, side, width, height):
    print(image)
    if side == "left":
        return image.crop((0, 0, width, height))
    elif side == "middle":
        left = (image.width - width) // 2
        return image.crop((left, 0, left + width, height))
    elif side == "right":
        return image.crop((image.width - width, 0, image.width, height))
    else:
        raise ValueError("Invalid side specified")

def create_composite_image(folder_path, output_path, side):
    print("entered create_composite_image")
    # Get a list of all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

    # Open the first image to get its dimensions
    first_image_path = os.path.join(folder_path, image_files[0])
    first_image = Image.open(first_image_path)
    output_width = first_image.width // len(image_files)
    output_height = first_image.height

    # Create a new image with the dimensions of the first image
    composite_image = Image.new('RGB', (first_image.width, output_height))

    # Paste each cropped image onto the composite image
    for i, image_file in enumerate(image_files):
        image = Image.open(os.path.join(folder_path, image_file))

        # Crop the specified portion of the image
        cropped_image = crop_side(image, side, output_width, output_height)

        # Paste the cropped image onto the composite image
        composite_image.paste(cropped_image, (i * output_width, 0))

    # Save the composite image
    composite_image.save(output_path)
    composite_image.show()

# Prompt the user to select a folder containing images
folder_path = select_folder()

# Ask the user if they want to use the center of the images
user_input_center = messagebox.askyesno("Select Side", "Do you want to use the center of the images?")
if user_input_center:
    side = "middle"
else:
    # If not, ask if they want to use the left side of the images
    user_input_left = messagebox.askyesno("Select Side", "Do you want to use the left side of the images?")
    if user_input_left:
        side = "left"
    else:
        # If not, inform the user that the right side will be used
        messagebox.showinfo("Side Selection", "The right side of the images will be used.")
        side = "right"   


# Define the output path for the composite image
output_path = 'composite_image_MicksSlide_right.jpg'

# Create the composite image
create_composite_image(folder_path, output_path, side)
