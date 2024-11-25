import math
from Bitmap255 import *
import threading
import tkinter as tk

# SpringyDotsApplet.java is the main code for this applet.
# It includes code to display the applet, handle user interaction,
# and animate the 3 Dots object.

# SpringyObject.java is support code that simulates
# the behavior of springs and masses.

# Bitmap255.java is a library that handles the drawing of trails on screen.

# ************** Global Values **************

class Global:
    spring_constant = 1000
    damping = 0.5
    mass = 1
    spring_min = 0.5
    spring_max = 2.0
    v_constant = 1000000.0
    time_interval = 0.01


# ************** Mass **************

class Mass:
    def __init__(self, x: int, y: int):
        self.m = Global.mass
        self.x = float(x)
        self.y = float(y)
        self.vX = 0.0
        self.vY = 0.0
        self.pressed = False
        self.movable = True
        self.visible = True

    def apply_force(self, forceX: float, forceY: float):
        self.vX += Global.time_interval * forceX / self.m
        self.vY += Global.time_interval * forceY / self.m

    def calculate_new_positions(self):
        if not self.movable or self.pressed:
            self.vX = 0.0
            self.vY = 0.0
        else:
            self.x += self.vX * Global.time_interval
            self.y += self.vY * Global.time_interval

    def set_movable(self, movable: bool):
        self.movable = movable

    def set_mass(self, mass: int):
        self.m = mass

    def distance_to(self, px: int, py: int) -> float:
        return math.sqrt((self.x - px) ** 2 + (self.y - py) ** 2)

class Spring:
    def __init__(self, m1, m2):
        self.spring_constant = Global.spring_constant
        self.visible = True
        self.mass1 = m1
        self.mass2 = m2
        # used for calculations
        self.spring_len = 0.0
        self.spring_min_len = 0.0
        self.spring_max_len = 0.0
        self.tension = 0.0
        self.lenX = 0.0
        self.lenY = 0.0
        self.len_now = 0.0
        self.newlenX = 0.0
        self.newlenY = 0.0
        self.newlen_now = 0.0
        self.f = 0.0
        self.fX = 0.0
        self.fY = 0.0

        lenX = m1.x - m2.x
        lenY = m1.y - m2.y
        self.spring_len = math.sqrt((lenX * lenX) + (lenY * lenY))
        self.spring_min_len = self.spring_len * Global.spring_min
        self.spring_max_len = self.spring_len * Global.spring_max

    def calculate_force(self):
        self.lenX = self.mass2.x - self.mass1.x
        self.lenY = self.mass2.y - self.mass1.y
        self.len_now = math.sqrt(self.lenX * self.lenX + self.lenY * self.lenY)
        self.newlenX = self.lenX + ((self.mass2.vX - self.mass1.vX) / Global.v_constant)
        self.newlenY = self.lenY + ((self.mass2.vY - self.mass1.vY) / Global.v_constant)
        self.newlen_now = math.sqrt(self.newlenX * self.newlenX + self.newlenY * self.newlenY)
        self.f = (Global.damping * Global.v_constant * (self.newlen_now - self.len_now)) / self.len_now
        self.fX = (self.lenX * self.f) / self.len_now
        self.fY = (self.lenY * self.f) / self.len_now

        # change velocity of masses
        self.mass1.apply_force(self.fX, self.fY)
        self.mass2.apply_force(-self.fX, -self.fY)

        # cap the length
        if self.len_now < self.spring_len / 2.0:
            self.len_now = self.spring_len / 2.0
        elif self.len_now > self.spring_len * 3.0 / 2.0:
            self.len_now = self.spring_len * 3.0 / 2.0

        # calculate tension of spring based on length
        self.tension = (self.spring_constant * (self.spring_len - self.len_now)) / self.spring_len

        # calculate force in x and y directions
        self.fX = (self.lenX * self.tension) / self.len_now
        self.fY = (self.lenY * self.tension) / self.len_now

        # apply the force to the masses
        self.mass1.apply_force(-self.fX, -self.fY)
        self.mass2.apply_force(self.fX, self.fY)

    def set_visible(self, v):
        self.visible = v


class SpringyObject:
    def __init__(self):
        self.masses = []
        self.springs = []
        self.drag_mass = None
        self.s = None
        self.m = None
        self.prev_x = 0.0
        self.prev_y = 0.0

    def add_mass(self, mass):
        self.masses.append(mass)

    def add_spring(self, spring):
        self.springs.append(spring)

    def grab(self, x, y):
        for m in self.masses:
            if m.distance_to(x, y) < 35:
                m.pressed = True
                self.drag_mass = m
                break
        if self.drag_mass:
            self.prev_x = self.drag_mass.x
            self.prev_y = self.drag_mass.y
        return True

    def drag(self, x, y):
        if self.drag_mass:
            self.prev_x = self.drag_mass.x
            self.prev_y = self.drag_mass.y
            self.drag_mass.x = x
            self.drag_mass.y = y
        return True

    def release(self, x, y):
        if self.drag_mass:
            self.drag_mass.pressed = False
            self.drag_mass.vX = 20 * (x - self.prev_x)
            self.drag_mass.vY = 20 * (y - self.prev_y)
            self.drag_mass = None
        return True

    def move(self):
        # Calculate spring forces
        for spring in self.springs:
            spring.calculate_force()

        # Calculate new Mass positions
        for mass in self.masses:
            mass.calculate_new_positions()
            

class SpringyDots(SpringyObject):
    def __init__(self):
        super().__init__()

        # Three masses connected by springs
        m0 = Mass(300, 270)  # center point (fixed)
        m1 = Mass(170, 320)  # left
        m2 = Mass(300, 320)  # middle
        m3 = Mass(360, 320)  # right

        self.add_mass(m0)
        self.add_mass(m1)
        self.add_mass(m2)
        self.add_mass(m3)

        m0.set_movable(False)
        m0.set_mass(2)
        m1.set_mass(2)
        m2.set_mass(5)
        m3.set_mass(3)

        s = Spring(m0, m2)
        s.set_visible(False)
        s.spring_constant = 500  # very mushy
        self.add_spring(s)

        s = Spring(m1, m2)
        s.spring_constant = 1000  # medium
        self.add_spring(s)

        s = Spring(m2, m3)
        s.spring_constant = 3000  # stiffer
        self.add_spring(s)
        
class SpringyDotsPanel(tk.Canvas, threading.Thread):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height)
        self.width = width
        self.height = height
        self.dots = SpringyDots()
        self.springs = self.dots.springs
        self.masses = self.dots.masses
        self.counter = 40000
        self.BMP = Bitmap255(master, width, height)
        self.pack()
        self.bind("<ButtonPress-1>", self.mouse_down)
        self.bind("<B1-Motion>", self.mouse_drag)
        self.bind("<ButtonRelease-1>", self.mouse_up)
        self.thread = None

    def mouse_down(self, event):
        self.dots.grab(event.x, event.y)

    def mouse_drag(self, event):
        self.dots.drag(event.x, event.y)

    def mouse_up(self, event):
        self.dots.release(event.x, event.y)

    def paint(self):
        self.dots.move()

        # Draw trails into image
        for s in self.springs:
            if s.visible:
                self.BMP.draw_line(int(s.mass1.x), int(s.mass1.y), int(s.mass2.x), int(s.mass2.y))

        # Draw image to screen
        self.BMP.paint(self)

        # Switch drawing from dark to light periodically
        if self.counter <= 0:
            self.BMP.target_color_value = 255.0 if self.BMP.target_color_value == 0.0 else 0.0
            self.counter = 40000
        self.counter -= 1

        # Draw springs to screen
        self.create_line(int(s.mass1.x), int(s.mass1.y), int(s.mass2.x), int(s.mass2.y), fill="green")

        # Draw masses: larger mass makes bigger circle
        for m in self.masses:
            r = m.m
            self.create_oval(m.x - r, m.y - r, m.x + r, m.y + r, outline="cyan")

    def update(self):
        self.paint()

    def start(self):
        if not self.thread:
            self.thread = threading.Thread(target=self.run)
            self.thread.start()

    def stop(self):
        self.thread = None

    def run(self):
        while self.thread:
            self.update()
            self.after(20)
            
class SpringyDotsApplet(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        #self.dot_panel = None
        self.master.configure(bg='darkgray')
        self.pack(fill="both", expand=True)
        self.dot_panel = SpringyDotsPanel(self, self.master.winfo_width(), self.master.winfo_height())

    def start(self):
        self.dot_panel.start()

    def stop(self):
        self.dot_panel.stop()

    def mouse_down(self, event):
        return self.dot_panel.mouse_down(event)

    def mouse_drag(self, event):
        return self.dot_panel.mouse_drag(event)

    def mouse_up(self, event):
        return self.dot_panel.mouse_up(event)

    def update(self, g=None):
        self.paint(g)

    def paint(self, g=None):
        self.dot_panel.paint()

# To run the applet equivalent in Python, you would typically use Tkinter's main loop
if __name__ == "__main__":
    root = tk.Tk()
    app = SpringyDotsApplet(master=root)
    app.mainloop()