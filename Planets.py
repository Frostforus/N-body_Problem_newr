from graphics import *
from math import log, sqrt


class Planet:
    __slots__ = ["name", "mass", "velocity", "position", "trail", "color", "outline_color", "ring", "fix",
                 "add_to_trail", "prev_acc", "prev_prev_acc"]

    def __init__(self, name, mass=1.0, velocity=None, position=None, color="white", outline_color="black", ring=0,
                 fix=False):
        self.name = name
        self.mass = mass
        self.velocity = [0, 0] if velocity is None else velocity
        self.position = [0, 0] if position is None else position
        self.color = color
        self.outline_color = outline_color
        self.ring = ring
        self.fix = fix
        self.trail = []
        self.add_to_trail = True
        self.prev_acc = [0, 0]
        self.prev_prev_acc = [0, 0]

    def get_radius(self):
        return max(sqrt(max(self.mass, 1)), 1)

    # Adds given velocity or position to current
    def update(self, velocity=None, position=None):
        if self.fix:
            return
        if velocity is None:
            self.velocity = self.velocity
        else:

            self.velocity[0] = self.velocity[0] + velocity[0]
            self.velocity[1] = self.velocity[1] + velocity[1]
        # TODO clear up code
        if position is None:
            self.position = self.position
        else:
            # FIXME when trail length is really high color is buggy
            if len(self.trail) >= 50:
                self.trail.pop(0)
            if self.add_to_trail:
                self.trail.append([float(self.position[0]), float(self.position[1])])
                self.add_to_trail = True
            else:
                self.add_to_trail = True

            self.position[0] = self.position[0] + position[0]
            self.position[1] = self.position[1] + position[1]

    # TODO egyedi shapek kulon megrajzolása  végül egy draw ami meghívja az összeset, hogy a cometnek is legyen
    #  trailje !basically done!
    def draw(self, win, draw_trail=True):
        # If Planet has Ring draw it
        if self.ring:
            self.draw_ring(win)

        if self.trail:
            self.draw_trail(win)

        self.draw_planet(win)

    def draw_ring(self, win):
        temp_ring = Circle(Point(self.position[0], self.position[1]), self.ring)
        temp_ring.setFill("black")
        temp_ring.setOutline("white")
        temp_ring.draw(win)

        temp_ring = Circle(Point(self.position[0], self.position[1]), self.ring - 3)
        temp_ring.setFill("dark gray")
        temp_ring.setOutline("white")
        temp_ring.draw(win)

    def draw_planet(self, win):
        # Draw planet
        temp_circle = Circle(Point(self.position[0], self.position[1]), self.get_radius())
        temp_circle.setOutline(self.outline_color)
        temp_circle.setFill(self.color)
        temp_circle.draw(win)

    def draw_trail(self, win):
        i = 1
        last_point = [0, 0]
        last_point[0] = self.position[0]
        last_point[1] = self.position[1]
        div = 255 / max(len(self.trail), 1)
        while i <= len(self.trail):
            line = Line(Point(last_point[0], last_point[1]), Point(self.trail[-i][0], self.trail[-i][1]))
            line.setWidth(3)
            #  TODO add colorable trails
            line.setFill(color_rgb(int(max(125 - i * div, 0)), int(max(255 - i * div, 0)), int(max(125 - i * div, 0))))
            line.draw(win)
            last_point[0] = self.trail[-i][0]
            last_point[1] = self.trail[-i][1]
            i += 1

    def print(self):
        print("Name:\t\t", self.name)
        print("Mass:\t\t", self.mass)
        print("Velocity:\t", self.velocity)
        print("Position:\t", self.position, end="\n\n")


class Comet(Planet):
    def draw(self, win, size=0.1):
        self.draw_trail(win)
        self.draw_planet(win)

        line_end = [0, 0]
        line_end[0] = - self.velocity[1]
        line_end[1] = self.velocity[0]

        line = self.line_from_middle((self.position[0] - line_end[0] * (1 / size)),
                                     (self.position[1] - line_end[1] * (1 / size)))
        line.setFill("white")
        line.setWidth(2)
        line.draw(win)

        line_end_2 = [0, 0]
        line_end_2[0] = (line_end[0] + self.velocity[0]) / 2
        line_end_2[1] = (line_end[1] + self.velocity[1]) / 2

        bline = self.line_from_middle((self.position[0] - line_end_2[0] * (1 / size)),
                                      (self.position[1] - line_end_2[1] * (1 / size)))
        bline.setFill(color_rgb(66, 75, 150))
        bline.setWidth(1)
        bline.draw(win)

        temp_circle = Circle(Point(self.position[0], self.position[1]), self.get_radius())
        temp_circle.setOutline(self.outline_color)
        temp_circle.setFill(self.color)
        temp_circle.draw(win)

    def line_from_middle(self, to_x, to_y):
        return Line(Point(self.position[0], self.position[1]), Point(to_x, to_y))
