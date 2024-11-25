import tkinter as tk
import random
import threading
import time


class Point:
    """Class to represent a point in 2D space."""
    def __init__(self, x, y):
        self.x = x
        self.y = y


class ConnectApplet(tk.Canvas):
    def __init__(self, root, width, height):
        super().__init__(root, width=width, height=height, bg="white")
        self.pack()

        self.width = width
        self.height = height

        self.picture_image = tk.PhotoImage(width=width, height=height)
        self.create_image((0, 0), image=self.picture_image, anchor="nw")

        self.p = [
            Point(self.width // 2, 100),
            Point(self.width // 2 + 70, 170),
            Point(self.width // 2 - 70, 170),
        ]
        self.current = self.p[0]

        self.bind("<Button-1>", self.mouse_down)
        self.bind("<B1-Motion>", self.mouse_drag)

        self.running = True
        self.animation_thread = threading.Thread(target=self.run)
        self.animation_thread.start()

    def stop(self):
        """Stop the animation."""
        self.running = False
        self.animation_thread.join()

    def run(self):
        """Main animation thread."""
        while self.running:
            self.update_picture()
            self.repaint()
            time.sleep(0.02)

    def repaint(self):
        """Redraw the points on the canvas."""
        self.delete("all")
        self.create_image((0, 0), image=self.picture_image, anchor="nw")
        for point in self.p:
            self.create_oval(
                point.x - 5, point.y - 5, point.x + 5, point.y + 5,
                fill="red", outline="black"
            )

    def mouse_down(self, event):
        """Select the nearest point when clicked."""
        shortest = float("inf")
        for point in self.p:
            d2 = (point.x - event.x) ** 2 + (point.y - event.y) ** 2
            if d2 <= shortest:
                self.current = point
                shortest = d2

    def mouse_drag(self, event):
        """Move the selected point by dragging."""
        self.current.x = event.x
        self.current.y = event.y
        self.repaint()

    def update_picture(self):
        """Update the image with new colors."""
        for _ in range(5000):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            a1 = self.f(self.p[0], self.p[1], x, y)
            a2 = self.f(self.p[1], self.p[2], x, y)
            a3 = self.f(self.p[2], self.p[0], x, y)

            if a1 * a2 * a3 > 0:
                color = "#FFFFFF" if a1 * a2 > 0 and a2 * a3 > 0 else "#BEBEBE"
            else:
                color = "#000000"

            self.picture_image.put(color, (x, y))

    def f(self, p1, p2, x, y):
        """Calculate the determinant for the triangle."""
        return ((p1.x - x) * (p2.y - y) - (p1.y - y) * (p2.x - x)) // 13


def main():
    root = tk.Tk()
    root.title("ConnectApplet")
    applet = ConnectApplet(root, width=800, height=600)
    root.protocol("WM_DELETE_WINDOW", applet.stop)
    root.mainloop()


if __name__ == "__main__":
    main()
