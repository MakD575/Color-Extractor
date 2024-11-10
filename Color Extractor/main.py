import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
from sklearn.cluster import KMeans


# Function to extract top N colors in hex format
def extract_top_colors(image_path, n_colors=10):
    try:
        # Load the image
        img = Image.open(image_path)
        img = img.convert("RGB")  # Ensure the image is in RGB format
        img = img.resize((img.width // 10, img.height // 10))  # Resize for faster processing

        # Convert image to numpy array
        img_array = np.array(img)
        img_array = img_array.reshape((-1, 3))  # Flatten the image into a 2D array

        # Perform k-means clustering to find the top N colors
        kmeans = KMeans(n_clusters=n_colors, random_state=42)
        kmeans.fit(img_array)

        # Get the cluster centers (top colors)
        colors = kmeans.cluster_centers_.astype(int)

        # Convert to hex format
        hex_colors = [rgb_to_hex(color) for color in colors]

        return colors, hex_colors
    except Exception as e:
        messagebox.showerror("Error", f"Error processing the image: {str(e)}")
        return [], []


# Convert RGB to Hex format
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


# Function to update the listbox with the hex colors and display their color swatches
def update_color_list(colors, hex_colors):
    # Clear current list
    color_listbox.delete(0, tk.END)

    for i, hex_color in enumerate(hex_colors):
        # Create a color swatch and display the color with the hex code side by side
        color_frame = tk.Frame(color_listbox)
        color_swatch = tk.Label(color_frame, bg=hex_color, width=4, height=2)
        color_swatch.pack(side=tk.LEFT, padx=5)
        color_code = tk.Label(color_frame, text=hex_color, width=10, font=('Arial', 12))
        color_code.pack(side=tk.LEFT)

        color_frame.pack(pady=5, fill=tk.X)


# Function to open file dialog and process the image
def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        colors, hex_colors = extract_top_colors(file_path, n_colors=10)
        if hex_colors:
            update_color_list(colors, hex_colors)


# Set up the Tkinter GUI
root = tk.Tk()
root.title("Top 10 Colors Extractor in Hex")

# Frame for the Listbox and Scrollbar
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Canvas for displaying the colors and hex codes
color_listbox = tk.Canvas(frame, width=400, height=300)
color_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for the canvas
scrollbar = tk.Scrollbar(frame, orient="vertical", command=color_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Link the scrollbar to the canvas
color_listbox.config(yscrollcommand=scrollbar.set)

# Button to open image
button = tk.Button(root, text="Open Image", command=open_image, font=('Arial', 14), bg='#4CAF50', fg='white')
button.pack(pady=20)

# Start the GUI loop
root.mainloop()


