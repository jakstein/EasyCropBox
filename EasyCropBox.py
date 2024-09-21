import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import os
import glob

class ImageCropper:
    """
    ImageCropper is a class that provides functionality for cropping images using a graphical user interface.
    Attributes:
        root (tk.Tk): The main application window.
        canvas (tk.Canvas): The canvas where the image is displayed and cropping is done.
        image (PIL.Image): The currently loaded image.
        tk_image (ImageTk.PhotoImage): The Tkinter-compatible image for display.
        image_path (str): The file path of the currently loaded image.
        image_list (list): A list of image file paths for navigation.
        current_image_index (int): The index of the currently displayed image in image_list.
        crop_rect (list): Coordinates of the cropping rectangle.
        rect_id (int): The ID of the rectangle drawn on the canvas.
    Methods:
        drop(event): Handles the drop event for loading an image.
        load_image(file_path): Loads an image from the specified file path and displays it.
        display_image(): Resizes and displays the current image on the canvas.
        start_crop(event): Initializes the cropping rectangle on mouse button press.
        update_crop(event): Updates the cropping rectangle as the mouse is dragged.
        end_crop(event): Finalizes the cropping rectangle on mouse button release.
        save_crop(): Crops the image based on the cropping rectangle and saves it.
        load_prev_image(): Loads the previous image from the image list.
        load_next_image(): Loads the next image from the image list.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropper")
        self.root.state("zoomed") 

        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill="both", expand=True)

        self.image = None
        self.tk_image = None
        self.image_path = ""
        self.image_list = []
        self.current_image_index = 0

        self.crop_rect = None
        self.rect_id = None
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.canvas.bind("<ButtonPress-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.update_crop)
        self.canvas.bind("<ButtonRelease-1>", self.end_crop)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack()

        self.prev_button = tk.Button(self.control_frame, text="<", command=self.load_prev_image, width=int(screen_width*0.005), height=int(screen_height*0.002)) 
        self.prev_button.pack(side="left")

        self.save_button = tk.Button(self.control_frame, text="Save Crop", command=self.save_crop, width=int(screen_width*0.015), height=int(screen_height*0.002))
        self.save_button.pack(side="left")

        self.next_button = tk.Button(self.control_frame, text=">", command=self.load_next_image, width=int(screen_width*0.005), height=int(screen_height*0.002))
        self.next_button.pack(side="left")

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop)

        # key bindings
        self.root.bind("a", lambda event: self.load_prev_image())
        self.root.bind("d", lambda event: self.load_next_image())
        self.root.bind("<space>", lambda event: self.save_crop())

    def drop(self, event):
        file_path = event.data.strip('{}')
        self.load_image(file_path)

    def load_image(self, file_path):
        self.image_path = file_path
        with Image.open(file_path) as img:
            if img.format != 'PNG':
                img = img.convert('RGBA')
                img.save(file_path, 'PNG')
            self.image = img
            self.display_image()

    def display_image(self):
        # fit the canvas
        canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        img_width, img_height = self.image.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        self.new_size = (int(img_width * ratio), int(img_height * ratio))
        resized_image = self.image.resize(self.new_size, Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized_image)

        # align the image at the center
        self.canvas.delete("all")
        self.canvas.create_image(
            (canvas_width - self.new_size[0]) // 2,
            (canvas_height - self.new_size[1]) // 2,
            anchor="nw",
            image=self.tk_image
        )
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def start_crop(self, event):
        self.crop_rect = [event.x, event.y, event.x, event.y]
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(*self.crop_rect, outline="red", width=2, dash=(2, 2))

    def update_crop(self, event):
        x1, y1 = self.crop_rect[0], self.crop_rect[1]
        x2, y2 = event.x, event.y

        # limit crop rectangle size
        canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        offset_x = (canvas_width - self.new_size[0]) // 2
        offset_y = (canvas_height - self.new_size[1]) // 2

        x2 = max(min(x2, offset_x + self.new_size[0]), offset_x)
        y2 = max(min(y2, offset_y + self.new_size[1]), offset_y)

        self.crop_rect = [x1, y1, x2, y2]
        self.canvas.coords(self.rect_id, *self.crop_rect)

    def end_crop(self, event):
        self.update_crop(event)

    def save_crop(self):
        if not self.crop_rect:
            return

        # calculate actual crop coordinates in the original image
        canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        img_width, img_height = self.image.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        offset_x = (canvas_width - int(img_width * ratio)) // 2
        offset_y = (canvas_height - int(img_height * ratio)) // 2

        coords_offsets = zip(self.crop_rect, [offset_x, offset_y, offset_x, offset_y])
        # calculate the actual crop coordinates in the original image
        x1, y1, x2, y2 = [int((coord - offset) / ratio) for coord, offset in coords_offsets]
        # ensure that "left" < "right" and "top" < "bottom"
        x1, x2, y1, y2 = sorted([x1, x2]) + sorted([y1, y2])
        
        cropped_image = self.image.crop((x1, y1, x2, y2))
        cropped_image.save(self.image_path, 'PNG')
        self.image = cropped_image  # change the current image to the cropped one
        self.display_image()  # refresh the canvas with the cropped image

    def load_prev_image(self):
        if self.image_list and self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_image(self.image_list[self.current_image_index])

    def load_next_image(self):
        if self.image_list and self.current_image_index < len(self.image_list) - 1:
            self.current_image_index += 1
            self.load_image(self.image_list[self.current_image_index])

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageCropper(root)
    root.mainloop()
