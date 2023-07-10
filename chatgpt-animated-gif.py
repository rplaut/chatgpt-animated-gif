import glob
import numpy as np
from PIL import Image
import imageio

# Define function for crossfading images
def crossfade_images(image1, image2, steps):
    # Convert images to numpy arrays
    img1_arr = np.array(image1)
    img2_arr = np.array(image2)

    # Initialize a list to hold the crossfaded images
    crossfaded_images = []

    # Create the crossfade transition
    for step in range(steps):
        alpha = step / float(steps)  # Calculate the current alpha
        img1_blend = img1_arr * (1 - alpha)  # Blend img1
        img2_blend = img2_arr * alpha  # Blend img2
        crossfaded_image = Image.fromarray(np.uint8(img1_blend + img2_blend))  # Add the blended images together
        crossfaded_images.append(crossfaded_image)

    return crossfaded_images

# Get the list of image files
image_files = sorted(glob.glob("street-fighter-*.png"))  # Change this to the correct path

# Initialize a list to hold the final sequence of images
final_images = []

# Adjust the steps to match the 1 second transition time, assuming a frame rate of 20 frames per second
transition_steps = 20

# Create a crossfade transition between each pair of images
for i in range(len(image_files) - 1):
    # Open the images
    img1 = Image.open(image_files[i]).convert("RGBA")
    img2 = Image.open(image_files[i + 1]).convert("RGBA")

    # Resize images to match the smallest image, this is necessary for crossfade
    min_width = min(img1.size[0], img2.size[0])
    min_height = min(img1.size[1], img2.size[1])
    img1 = img1.resize((min_width, min_height))
    img2 = img2.resize((min_width, min_height))

    # Create a crossfade transition between the images and add to final_images
    crossfaded_images = crossfade_images(img1, img2, steps=transition_steps)
    final_images.extend(crossfaded_images)

# Append the last image
final_images.append(Image.open(image_files[-1]).convert("RGBA"))

# Convert the final sequence of images into an animated GIF
gif_path = "street-fighter-animated-1sec.gif"
imageio.mimsave(gif_path, final_images, duration=0.05)
