import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, filedialog, Toplevel, Entry
from PIL import Image, ImageTk, ImageEnhance, ImageFilter

# Image processing functions
def linear_transform(image):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(1.5)

def logarithmic_transform(image):
    img_array = np.array(image).astype(np.float32)
    img_array = 255 * np.log1p(img_array) / np.log(256)
    return Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))

def power_law_transform(image, gamma=2.0):
    img_array = np.array(image).astype(np.float32) / 255.0
    img_gamma = np.power(img_array, gamma) * 255
    return Image.fromarray(np.clip(img_gamma, 0, 255).astype(np.uint8))

def thresholding(image, threshold=128):
    img_array = np.array(image.convert('L'))
    thresholded = (img_array > threshold) * 255
    return Image.fromarray(thresholded.astype(np.uint8))

def histogram_equalization(image):
    img_array = np.array(image.convert('L'))
    histogram, bins = np.histogram(img_array.flatten(), bins=256, range=[0, 256])
    cdf = histogram.cumsum()
    cdf_normalized = 255 * cdf / cdf[-1]
    img_equalized = np.interp(img_array.flatten(), bins[:-1], cdf_normalized)
    return Image.fromarray(img_equalized.reshape(img_array.shape).astype(np.uint8))

def smoothing(image):
    return image.filter(ImageFilter.SMOOTH)

def sharpening(image):
    return image.filter(ImageFilter.SHARPEN)

def edge_detection(image):
    return image.filter(ImageFilter.FIND_EDGES)

# Main Application Class
class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Application")
        self.root.geometry("800x600")
        
        self.image = None
        self.displayed_image = None

        # UI Components
        self.label = Label(root, text="Select an image to start", font=("Arial", 16))
        self.label.pack(pady=20)

        self.select_button = Button(root, text="Select Image", command=self.select_image)
        self.select_button.pack(pady=10)

        self.resize_button = Button(root, text="Resize Image", command=self.resize_image, state="disabled")
        self.resize_button.pack(pady=10)

        self.transform_button = Button(root, text="Apply Transformations", command=self.apply_transformations, state="disabled")
        self.transform_button.pack(pady=10)

        self.image_label = Label(root)
        self.image_label.pack()

    def select_image(self):
        # Open file dialog to select an image
        file_path = filedialog.askopenfilename(title="Select an Image File",
                                               filetypes=[("Image Files", "*.jpg;*.png;*.jpeg;*.bmp")])
        if file_path:
            self.image = Image.open(file_path)
            self.display_image(self.image)
            self.transform_button.config(state="normal")
            self.resize_button.config(state="normal")
        else:
            self.label.config(text="No image selected. Please try again.")

    def display_image(self, image):
        # Display the image in the main window without deformation
        original_width, original_height = image.size
        max_width, max_height = 400, 300
        scale = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        image_resized = image.resize((new_width, new_height))
        self.displayed_image = ImageTk.PhotoImage(image_resized)
        self.image_label.config(image=self.displayed_image)
        self.label.config(text="Image Loaded Successfully")

    def resize_image(self):
        if self.image:
            # Open a new window for resizing
            resize_window = Toplevel(self.root)
            resize_window.title("Resize Image")
            resize_window.geometry("400x200")

            Label(resize_window, text="Enter new width:").pack(pady=10)
            width_entry = Entry(resize_window)
            width_entry.pack(pady=5)

            def apply_resize():
                try:
                    new_width = int(width_entry.get())
                    original_width, original_height = self.image.size
                    aspect_ratio = original_height / original_width
                    new_height = int(new_width * aspect_ratio)
                    resized_image = self.image.resize((new_width, new_height))
                    self.image = resized_image
                    self.display_image(self.image)
                    resize_window.destroy()
                except ValueError:
                    Label(resize_window, text="Invalid width. Please enter a number.", fg="red").pack()

            Button(resize_window, text="Apply", command=apply_resize).pack(pady=10)

    def apply_transformations(self):
        if self.image:
            # Open a new window to display transformations
            transform_window = Toplevel(self.root)
            transform_window.title("Image Transformations")
            transform_window.geometry("1200x800")

            # Apply transformations
            transformations = {
                "Original": self.image,
                "Linear Transform": linear_transform(self.image),
                "Logarithmic Transform": logarithmic_transform(self.image),
                "Power Law Transform (Gamma=2.0)": power_law_transform(self.image),
                "Thresholding": thresholding(self.image),
                "Histogram Equalization": histogram_equalization(self.image),
                "Smoothing": smoothing(self.image),
                "Sharpening": sharpening(self.image),
                "Edge Detection": edge_detection(self.image),
            }

            # Display transformations in the new window
            for i, (name, transformed_image) in enumerate(transformations.items()):
                img_resized = transformed_image.resize((200, 150))
                img_display = ImageTk.PhotoImage(img_resized)
                label = Label(transform_window, text=name)
                label.grid(row=i // 3 * 2, column=i % 3, padx=10, pady=10)
                image_label = Label(transform_window, image=img_display)
                image_label.image = img_display  # Keep a reference to avoid garbage collection
                image_label.grid(row=i // 3 * 2 + 1, column=i % 3, padx=10, pady=10)

# Run the application
if __name__ == "__main__":
    root = Tk()
    app = ImageProcessingApp(root)
    root.mainloop()
