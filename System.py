import time
from math import pi, cos, sin, sqrt

from Planets import Planet, Comet
from graphics import GraphWin, update


class System:
    __slots__ = ["name", "size", "max_planets", "planets", "gamma", "scale", "max_time", "collisions"]

    def __init__(self, name="Sol system", size=500, max_planets=3, gamma=20, scale=1, max_time=100, symmetry=0):
        self.name = name
        self.size = size
        self.max_planets = max_planets
        self.planets = []
        self.gamma = gamma
        self.scale = scale
        self.max_time = max_time
        self.collisions = 0
        if not symmetry:
            # TODO add frame of reference
            self.add_planets(Planet(name="Sôl", mass=2500, color="yellow", fix=False),
                             Planet(name="Mercury", mass=1.5, velocity=[0, 20], position=[100, 0], color="grey"),
                             Planet(name="Venus", mass=1.85, velocity=[0, -15], position=[-150, 0]),
                             Planet(name="Terra", mass=2, velocity=[-10, 0], position=[0, 290], color="blue"),
                             Planet(name="Mars", mass=1.2, velocity=[15, 0], position=[0, -290], color="orange"),
                             Planet(name="Iuppiter", mass=200, velocity=[5, -5], position=[-300, -290], color="brown"),
                             Planet(name="Saturnus", mass=150, velocity=[-5, 5], position=[300, 290], color="Yellow",
                                    ring=25),
                             Comet("Halley's Comet", mass=0, velocity=[4, 4], position=[300, -290], color="light blue"),
                             Planet(name="Saturnus", mass=150, velocity=[0, 20], position=[500, -500], color="Yellow")
                             )
        else:
            self.add_planets(Planet(name="Sol", mass=1000, color="red", fix=True))
            for i in range(max_planets - 1):
                self.add_planets(
                    Planet(name=i, mass=0, velocity=self.point_velocity(sqrt((10 * gamma * self.planets[0].mass)/symmetry) , i, max_planets - 1),
                           position=self.point(symmetry, i, max_planets - 1), color="white"))

    def point(self, r, currentpoint, totalpoints):
        theta = pi * 2 / totalpoints
        angle = theta * currentpoint
        position = [r * cos(angle), r * sin(angle)]
        return position

    def point_velocity(self, speed, currentpoint, totalpoints):
        theta = pi * 2 / totalpoints
        angle = theta * currentpoint
        position = [speed * cos(angle + pi / 2), speed * sin(angle + pi / 2)]
        return position

    def add_planets(self, *args):
        for planet in args:
            if len(self.planets) < self.max_planets:
                self.planets.append(planet)
            else:
                print("Too many Planets")

    # TODO: Collide function; if the two planets are closer than then sum of their radius then the smaller ones mass
    #  is added to the larger ones, while it is destroyed
    def collide(self, planet_1, planet_2):
        if sqrt((planet_1.position[0] - planet_2.position[0]) ** 2 + (
                planet_1.position[1] - planet_2.position[1]) ** 2) < planet_1.get_radius() + planet_2.get_radius():
            print(planet_1.name, " and ", planet_2.name, "collided.")
            self.collisions += 1
            if planet_1.mass < planet_2.mass:
                self.planets.remove(planet_1)
                planet_2.mass += planet_1.mass
                print(planet_2.name, "'s new mass: ", planet_2.mass, " kg")
            else:
                self.planets.remove(planet_2)
                planet_1.mass += planet_2.mass
                print(planet_1.name, "'s new mass: ", planet_1.mass, " kg")

    def update(self, simulation_speed=1.0):
        # runs through all the planets
        for i in self.planets:

            # move based on last velocity

            i.update(position=i.velocity)
            # temp array
            calc_arr = []
            for p in self.planets:
                calc_arr.append(p)
            calc_arr.remove(i)
            # Physics calculation

            forces_array = []
            for p in calc_arr:
                self.collide(i, p)
                if p.mass != 0:
                    r = sqrt((i.position[0] - p.position[0]) ** 2 + (i.position[1] - p.position[1]) ** 2)

                    # Calculates the force on current object towards the other object
                    force_magnitude = self.gamma * (max(i.mass, 1) * p.mass) * -1 / (r ** 2)

                    force = [0, 0]
                    force[0] = (i.position[0] - p.position[0]) * force_magnitude / r
                    force[1] = (i.position[1] - p.position[1]) * force_magnitude / r
                    forces_array.append(force)

            current_acc = [0, 0]
            for f in range(len(forces_array)):
                if f == 0:
                    current_acc[0] = forces_array[0][0] / (max(i.mass, 1))
                    current_acc[1] = forces_array[0][1] / (max(i.mass, 1))

                else:
                    current_acc[0] += forces_array[f][0] / (max(i.mass, 1))
                    current_acc[1] += forces_array[f][1] / (max(i.mass, 1))



            current_acc[0] /= simulation_speed
            current_acc[1] /= simulation_speed
            i.update(velocity=current_acc)

    def print(self, win, printstuff=False):

        for i in self.planets:
            i.draw(win)
            if printstuff:
                i.print()

    def start_simulation(self, simulation_speed=1, framerate=30):
        # Header initializes window
        simulation_speed = 1 / simulation_speed

        win_name = self.name + " - N-Body Problem"
        win = GraphWin(win_name, self.size, self.size, autoflush=False)
        pos_x = 50
        pos_y = 25
        win.master.geometry('%dx%d+%d+%d' % (self.size, self.size, pos_x, pos_y))
        win.setBackground("black")
        win.setCoords(-self.size / (2 * self.scale), -self.size / (2 * self.scale), self.size / (2 * self.scale),
                      self.size / (2 * self.scale))

        # Body
        start_time = time.time()
        current_time = time.time()
        draw_time = time.time()

        while win.checkMouse() is None:
            # FIXME this should be drawspeed
            if simulation_speed < time.time() - current_time:

                current_time = time.time()
                # draw update to window
                win.delete("all")
                # TODO ezen belul legyen
                self.update(simulation_speed)
                self.print(win)
            # If max time is exceeded break out of loop
            else:
                continue

            # Max time reached stop simulation
            if self.max_time < time.time() - start_time:
                break

            # If time passed is greater than refresh rate, refresh
            # TODO lehet ezt az updaten belul kulon is kene kezelni
            update(framerate)

        # Trailer closes window
        win.close()
        if not self.collisions:
            print("Simulation successful; System Stable")
        else:
            print("Simulation over; System Unstable\nCollisions: ", self.collisions)
