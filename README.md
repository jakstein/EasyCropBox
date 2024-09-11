# Easy Image Crop Box

Image Cropper is a simple, bloat free Python application that allows users to crop images using a GUI. The application supports drag-and-drop functionality for loading images and source folder and provides basic controls for navigating through images and saving cropped sections. Made for learning purposes.

## Features

- Drag-and-drop image loading
- Crop images using a crosshair cursor
- Navigate through images in a directory
- Save cropped images

## Requirements

- Python 3.x
- `tkinter`
- `tkinterdnd2`
- `Pillow`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/image-cropper.git
    cd image-cropper
    ```

2. Install the required packages:
    ```sh
    pip install tkinterdnd2 Pillow
    ```

## Usage

1. Run the application:
    ```sh
    python CropBox.py
    ```

2. Drag and drop an image file onto the application window to load it. The image directory will be loaded too, allowing you to move to next and previous images within the same folder.

3. Use the mouse to draw a rectangle around the area you want to crop:
    - Click and hold the left mouse button to start the crop.
    - Drag the mouse to adjust the crop area.
    - Release the left mouse button to finalize the crop area.

4. Use the control buttons or keyboard shortcuts to navigate and save:
    - `<` button or `a`
    - `>` button or `d`
    - `Save Crop` button or `space`

## License

This project is licensed under the MIT License. See the LICENSE file for details.

