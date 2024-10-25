import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random
import os

class ClickTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Organic Matter Detector")
        
        # Set up the canvas
        self.canvas = tk.Canvas(master, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.line = [] # Store points for each object
        self.points = [] # Store points of current object
        self.width = [] # Store widths for each line
        self.line_width = 1  # Default line width
        
        # Bind left-click
        self.canvas.bind("<Button-1>", self.track_click)

        # Button to open an image
        self.open_button = tk.Button(master, text="Open Image", command=self.open_image)
        self.open_button.pack()

        # Button to save coordinates
        self.save_button = tk.Button(master, text="Save Coordinates", command=self.save_coordinates)
        self.save_button.pack()

        # Button to make new line for new object
        self.new_button = tk.Button(master, text="New Line", command=self.save_coordinates)
        self.new_button.pack()

        # Clear coordinates in cases of misclicks or inaccurate clicks
        self.clear_button = tk.Button(master, text="Clear Points", command=self.clear_coordinates)
        self.clear_button.pack()

        # Create a line width slider
        self.line_width_slider = tk.Scale(master, from_=1, to=10, orient=tk.HORIZONTAL, label="Line Width")
        self.line_width_slider.set(self.line_width)  # Set default value
        self.line_width_slider.pack()

        # File name to use to make new coordinate file
        self.file_name = ""

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg")])
        if file_path:
            # Load the image and resize to standard
            self.image = Image.open(file_path)
            self.image = self.image.resize((600, 600))
            self.photo = ImageTk.PhotoImage(self.image)
            
            self.canvas.delete("all")
            self.canvas.config(width=self.photo.width(), height=self.photo.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

            # Reset lines and points for new image
            self.points = []
            self.line = []
        
        # Get file name
        file_path = os.path.basename(file_path) # Returns base name
        file_path = os.path.splitext(file_path)[0] # Splits into a tuple, first index is name, second index is the extension
        self.file_name = file_path

    def clear_coordinates(self):
        self.canvas.delete(self.points)
        self.points.clear()

    def random_color(self):
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))
    
    def track_click(self, event): # Track clicks and draw lines between coordinates
        x, y = event.x, event.y
        self.points.append((x, y))
        self.draw_lines('red', self.points)

    def draw_lines(self, color, coordinates): # Draw the lines connecting the points
        self.canvas.create_line(coordinates, fill=color, width=self.line_width_slider.get(), tags="lines")


    def save_coordinates(self):
        self.line.append(self.points)
        self.draw_lines(self.random_color(), self.line[-1]) # Add current line coordinates to line list
        with open(self.file_name, "a") as f: # Make or append to file
            f.write(f"Object {len(self.line)}\n")
            for point in self.points:
                f.write(f"{point[0]}, {point[1]}\n")
            f.write(f"Line Width: {self.line_width_slider.get()}\n\n")
        print("Coordinates saved to coordinates.txt")
        self.width.append(self.line_width_slider.get()) # Add width to list to track line widths
        self.points.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickTracker(root)
    root.mainloop()
