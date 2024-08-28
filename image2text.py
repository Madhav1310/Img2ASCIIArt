from PIL import Image
import numpy as np
import requests
from io import BytesIO

# Global Constants
TXT_FILE = 'outputs/recent_output.txt'
IMAGE_PATH = 'inputs/Rick.jpg'  # User must place the image in the 'inputs' folder and change this path
ASCII_CHARS = '@@##MMBB88NNHHOOGGPPEEXXFFVVYY22ZZCC77LLjjll11rrii;;;:::....  '
LUMINOSITY_SCALE = 256 / len(ASCII_CHARS)
WIDTH = 50  # User can change this width for different outputs

def remove_transparency(image, bg_color=(255, 255, 255)): #Removes transparency from an image by replacing it with a specified background color.
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        alpha = image.convert('RGBA').split()[-1]
        bg = Image.new("RGBA", image.size, bg_color + (255,))
        bg.paste(image, mask=alpha)
        return bg.convert("RGB")
    return image

def load_image(image_path): #Loads an image from a local file path.
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def convert_to_grayscale(image): #Converts an image to grayscale.
    image = remove_transparency(image)
    return image.convert("L")

def resize_image(image, width): #Resizes an image while maintaining its aspect ratio.
    aspect_ratio = image.height / image.width
    height = int(width * aspect_ratio / 2)  # Adjust height for ASCII character proportions
    return image.resize((width, height))

def map_pixels_to_ascii(image): #Converts grayscale pixels to ASCII characters.
    pixels = np.array(image)
    ascii_image = '\n'.join(
        ''.join(ASCII_CHARS[int(pixel / LUMINOSITY_SCALE)] for pixel in row)
        for row in pixels
    )
    return ascii_image

def save_ascii_image(ascii_image, txt_file_path): #Saves the ASCII art to a text file.
    with open(txt_file_path, 'w', encoding='utf-8') as file:
        file.write(ascii_image)

def main(): #Main function to handle the workflow.
    try:
        image = load_image(IMAGE_PATH)
        if image is None:
            return

        grayscale_image = convert_to_grayscale(image)
        resized_image = resize_image(grayscale_image, WIDTH)
        ascii_image = map_pixels_to_ascii(resized_image)
        save_ascii_image(ascii_image, TXT_FILE)

        print(ascii_image)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()