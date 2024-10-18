import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ClickTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Click Tracker")
        
        # Set up the canvas
        self.canvas = tk.Canvas(master, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.points = []
        self.line_width = 2  # Default line width
        
        self.canvas.bind("<Button-1>", self.track_click)


        # Button to open an image
        self.open_button = tk.Button(master, text="Open Image", command=self.open_image)
        self.open_button.pack()

        # Button to save coordinates
        self.save_button = tk.Button(master, text="Save Coordinates", command=self.save_coordinates)
        self.save_button.pack()
        
        # Create a line width slider
        self.line_width_slider = tk.Scale(master, from_=1, to=10, orient=tk.HORIZONTAL, label="Line Width")
        self.line_width_slider.set(self.line_width)  # Set default value
        self.line_width_slider.pack()

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg")])
        if file_path:
            # Load the image without modifying the original file
            self.image = Image.open(file_path)
            self.photo = ImageTk.PhotoImage(self.image)

            # Clear the canvas and display the image at its original size
            self.canvas.delete("all")
            self.canvas.config(width=self.photo.width(), height=self.photo.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

            # Reset points for a new image
            self.points = []

    def track_click(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.draw_lines()

    def draw_lines(self):
        self.canvas.delete("lines")  # Clear previous line drawings
        
        # Draw the lines connecting the points
        if len(self.points) > 1:
            self.canvas.create_line(self.points, fill='red', width=self.line_width_slider.get(), tags="lines")

    def save_coordinates(self):
        with open("coordinates.txt", "w") as f:
            for point in self.points:
                f.write(f"{point[0]}, {point[1]}\n")
            f.write(f"Line Width: {self.line_width_slider.get()}\n")
        print("Coordinates saved to coordinates.txt")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickTracker(root)
    root.mainloop()
