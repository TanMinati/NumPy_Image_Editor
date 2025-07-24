import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NumPy Image Editor")
        self.image_array = None

        # Buttons
        # Create a frame to hold buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)  # Adds vertical padding around the whole group

        # Row 0
        tk.Button(button_frame, text="Choose Image", command=self.load_image).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Save Image", command=self.save_image).grid(row=0, column=1, padx=10, pady=10)

        # Row 1
        tk.Button(button_frame, text="Grayscale", command=self.grayscale).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Rotate", command=self.rotate).grid(row=1, column=1, padx=10, pady=10)

        # Row 2
        tk.Button(button_frame, text="Flip Horizontal", command=self.flip_horizontal).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Flip Vertical", command=self.flip_vertical).grid(row=2, column=1, padx=10, pady=10)

        #Row 3
        tk.Button(button_frame, text="Sepia Filter", command=self.apply_sepia).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Inversion", command=self.inversion).grid(row=3, column=1, padx=10, pady=10)

        # Image display
        self.img_label = tk.Label(root)
        self.img_label.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.img = Image.open(file_path).convert("RGB")
            self.image_array = np.array(self.img)
            self.display_image(self.img)

    def display_image(self, img):
        img = img.resize((500, 500))  # Resize for preview
        tk_img = ImageTk.PhotoImage(img)
        self.img_label.config(image=tk_img)
        self.img_label.image = tk_img

    def grayscale(self):
        if self.image_array is not None:
            gray = np.dot(self.image_array[...,:3], [0.2989, 0.587, 0.114])
            gray_img = Image.fromarray(gray.astype(np.uint8))
            self.display_image(gray_img)
            self.image_array = np.stack([gray]*3, axis=-1).astype(np.uint8)

    def flip_horizontal(self):
        if self.image_array is not None:
            self.image_array = np.fliplr(self.image_array)
            self.display_image(Image.fromarray(self.image_array))

    def flip_vertical(self):
        if self.image_array is not None:
            self.image_array = np.flipud(self.image_array)
            self.display_image(Image.fromarray(self.image_array))

    def rotate(self):
        if self.image_array is not None:
            self.image_array = np.rot90(self.image_array)
            self.display_image(Image.fromarray(self.image_array))

    def apply_sepia(self):
        sepia_matrix = np.array([[0.393, 0.769, 0.189],
                                [0.349, 0.686, 0.168],
                                [0.272, 0.534, 0.131]])
        self.image_array= np.clip(self.image_array @ sepia_matrix.T, 0, 255).astype(np.uint8)
        self.display_image(Image.fromarray(self.image_array))

    def inversion(self):
        if self.image_array is not None:
            self.image_array=255-self.image_array
            self.display_image(Image.fromarray(self.image_array))
    
    def save_image(self):
        if self.image_array is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
            if file_path:
                Image.fromarray(self.image_array).save(file_path)

# Run the app
root = tk.Tk()
root.title("Numpy Image Editor")
app = ImageApp(root)
root.mainloop()
