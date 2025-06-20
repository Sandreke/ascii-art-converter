from PIL import Image
import numpy as np
import time
import tkinter as tk
import threading

def image_to_ascii(image_path, text_widget=None):
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        if text_widget:
            text_widget.insert(tk.END, f"Error: Image not found at path: {image_path}")
        else:
            print(f"Error: Image not found at path: {image_path}")
        return

    # Convert to grayscale
    if img.mode == 'RGBA':
        # Create a white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3]) # Use alpha channel as mask
        img = background

    img = img.convert("L")

    # Resize the image
    width, height = img.size
    aspect_ratio = height / width
    
    desired_width = 180 # Desired ASCII art width
    output_height = int(desired_width * aspect_ratio * 0.50) # 0.50 factor to correct character aspect ratio
    img = img.resize((desired_width, output_height))

    # Map pixels to ASCII characters
    pixels = np.array(img)
    
    # ASCII character set (from darkest to lightest)
    ascii_chars = """@@@###%%88&&W*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. """

    ascii_art = []
    for row in pixels:
        line = [ascii_chars[int((pixel / 255) * (len(ascii_chars) - 1))] for pixel in row]
        ascii_art.append("".join(line))
    
    if text_widget:
        text_widget.delete(1.0, tk.END) # Clear the text widget before drawing
        for line in ascii_art:
            text_widget.insert(tk.END, line + "\n")
            text_widget.update_idletasks() # Update the window
            time.sleep(0.08)
    else:
        for line in ascii_art:
            print(line)
            time.sleep(0.08)

def start_drawing(image_path, text_widget):
    thread = threading.Thread(target=image_to_ascii, args=(image_path, text_widget))
    thread.start()

# Input image path
input_image_path = "resources/cristiano.png"

if __name__ == "__main__":
    root = tk.Tk()
    root.title("My pretty girl <3 by Sandreke")
    root.state('zoomed') # Maximize the window at start
    root.configure(bg='white') # Set window background to white

    text_area = tk.Text(root, wrap='char', font=('Courier', 5), bg='white', fg='black', borderwidth=0, highlightthickness=0, relief='flat')
    text_area.pack(expand=True, fill='both', padx=20, pady=20)

    start_drawing(input_image_path, text_area)

    root.mainloop() 