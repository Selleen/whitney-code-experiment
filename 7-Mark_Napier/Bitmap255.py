import tkinter as tk
from tkinter import PhotoImage
import numpy as np

class Bitmap255(tk.Canvas):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height, bg="darkgray")
        self.winWidth = width
        self.winHeight = height
        self.winWidthCenter = self.winWidth // 2
        self.winHeightCenter = self.winHeight // 2
        self.maxBitmapIdx = self.winWidth * self.winHeight - 1
        self.targetColorValue = 255.0
        self.opacity = 0.05
        self.bgColorValue = 40
        self.frameData = np.full(self.winWidth * self.winHeight, self.bgColorValue, dtype=np.uint8)
        
        # Palette initialization
        self.palRed = np.zeros(256, dtype=np.uint8)
        self.palGreen = np.zeros(256, dtype=np.uint8)
        self.palBlue = np.zeros(256, dtype=np.uint8)
        self.build_palette(0.0)

        self.image = PhotoImage(width=self.winWidth, height=self.winHeight)
        self.create_image(0, 0, anchor="nw", image=self.image)

        # Set initial bounding box
        self.minX = self.winWidthCenter
        self.maxX = self.winWidthCenter
        self.minY = self.winHeightCenter
        self.maxY = self.winHeightCenter

    def set_opacity(self, opacity):
        if 0.0 <= opacity <= 1.0:
            self.opacity = opacity

    def make_fade(self, bR, bG, bB, eR, eG, eB, num_steps):
        steps = float(num_steps)
        for curr_step in range(int(steps)):
            ratio = curr_step / steps
            cR = int(bR * (1 - ratio) + eR * ratio)
            cG = int(bG * (1 - ratio) + eG * ratio)
            cB = int(bB * (1 - ratio) + eB * ratio)
            self.palRed[curr_step] = min(255, max(0, cR))
            self.palGreen[curr_step] = min(255, max(0, cG))
            self.palBlue[curr_step] = min(255, max(0, cB))

    def build_palette(self, t):
        self.make_fade(15, 20, 25, 255, 255, 200, 256)

    def update(self):
        self.paint()

    def paint(self):
        # Update image pixels
        for y in range(self.winHeight):
            for x in range(self.winWidth):
                idx = y * self.winWidth + x
                color_value = self.frameData[idx]
                self.image.put(f"#{self.palRed[color_value]:02x}{self.palGreen[color_value]:02x}{self.palBlue[color_value]:02x}", (x, y))

        # Reset bounding box to center
        self.minX = self.winWidthCenter
        self.maxX = self.winWidthCenter
        self.minY = self.winHeightCenter
        self.maxY = self.winHeightCenter

    def draw_line(self, x1, y1, x2, y2):
        deltaX = abs(x1 - x2)
        deltaY = abs(y1 - y2)
        xdir = 1 if x2 > x1 else -1
        ydir = 1 if y2 > y1 else -1
        if deltaX > deltaY:
            for dx in range(deltaX + 1):
                yspot = int(y1 * ((deltaX - dx) / deltaX) + y2 * (dx / deltaX))
                xspot = x1 + (xdir * dx)
                if 0 <= yspot < self.winHeight and 0 <= xspot < self.winWidth:
                    idx = yspot * self.winWidth + xspot
                    if 0 <= idx < self.maxBitmapIdx:
                        pixel = self.frameData[idx]
                        self.frameData[idx] = min(255, pixel + int((self.targetColorValue - pixel) * self.opacity))

        else:
            for dy in range(deltaY + 1):
                xspot = int(x1 * ((deltaY - dy) / deltaY) + x2 * (dy / deltaY))
                yspot = y1 + (ydir * dy)
                if 0 <= yspot < self.winHeight and 0 <= xspot < self.winWidth:
                    idx = yspot * self.winWidth + xspot
                    if 0 <= idx < self.maxBitmapIdx:
                        pixel = self.frameData[idx]
                        self.frameData[idx] = min(255, pixel + int((self.targetColorValue - pixel) * self.opacity))

        # Adjust bounding box
        self.minX = min(self.minX, x1, x2)
        self.maxX = max(self.maxX, x1, x2)
        self.minY = min(self.minY, y1, y2)
        self.maxY = max(self.maxY, y1, y2)

    def fill_rect(self, x, y, w, h):
        fade_radius = 2
        for y1 in range(int(y) - fade_radius, int(y) + fade_radius):
            for x1 in range(int(x) - fade_radius, int(x) + fade_radius):
                idx = y1 * self.winWidth + x1
                if 0 <= idx < self.maxBitmapIdx:
                    pixel = self.frameData[idx]
                    self.frameData[idx] = min(255, pixel + int((self.targetColorValue - pixel) * self.opacity))

#if __name__ == "__main__":
  #  root = tk.Tk()
   # bitmap = Bitmap255(root, 800, 600)
   # bitmap.pack()
   # root.mainloop()
