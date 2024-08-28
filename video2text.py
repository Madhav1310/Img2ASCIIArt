import cv2
from PIL import Image
import numpy as np
import time

# Global Constants
VIDEO_PATH = 'inputs/dance.mov'  # User must place the video in the 'inputs' folder and update this path
CHAR_WIDTH = 50  # User can change this width for different outputs

ASCII_CHARS = '@MWNHB8$06XFVYZ27>1jli!;:,. '
LUMINOSITY_SCALE = 256 / len(ASCII_CHARS)

def remove_transparency(image, bg_color=(255, 255, 255)):
    """Removes transparency from an image by replacing it with a specified background color."""
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        alpha = image.convert('RGBA').split()[-1]
        bg = Image.new("RGBA", image.size, bg_color + (255,))
        bg.paste(image, mask=alpha)
        return bg.convert("RGB")
    return image

def image_to_pixel_data(image, char_width=100):
    """Converts an image to grayscale and resizes it while maintaining aspect ratio."""
    image = image.convert("L")
    width, height = image.size
    resized_image = image.resize((char_width, int(char_width * (height / width) / 2.4)))
    return np.array(resized_image)

def pixel_data_to_ascii(pixel_data):
    """Maps grayscale pixel data to ASCII characters."""
    ascii_image = '\n\n'
    for row in pixel_data:
        for pixel in row:
            ascii_image += ASCII_CHARS[int(pixel / LUMINOSITY_SCALE)]
        ascii_image += '\n'
    return ascii_image + '\n'

def process_video(video_path, char_width=100):
    """Processes video frame by frame, converting each frame to ASCII art."""
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    print(f"Video Info - Width: {width}, Height: {height}, FPS: {fps}")

    while True:
        start_time = time.time()
        ret, frame = video_capture.read()
        if ret:
            pil_image = Image.fromarray(frame)
            pixel_data = image_to_pixel_data(pil_image, char_width=char_width)
            ascii_image = pixel_data_to_ascii(pixel_data)
            print(ascii_image)
        else:
            break

        time_to_sleep = (1 / fps) - (time.time() - start_time)
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

    video_capture.release()
    cv2.destroyAllWindows()

def main():
    """Main function to handle the video-to-ASCII conversion workflow."""
    process_video(VIDEO_PATH, CHAR_WIDTH)


main()