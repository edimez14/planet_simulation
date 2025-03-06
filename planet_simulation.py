import pygame
import math

pygame.init()

# `WIDTH, HEIGHT = 700, 700` is a Python statement that is assigning the values 700 to the variables
# `WIDTH` and `HEIGHT` simultaneously using tuple unpacking. This line is defining the width and
# height of the window where the planet simulation will be displayed.
WIDTH, HEIGHT = 700, 700

# `WIN = pygame.display.set_mode((WIDTH, HEIGHT))` is setting up the display window for the planet
# simulation with the specified width and height. The `pygame.display.set_mode()` function creates a
# window for displaying graphics, and it takes a tuple `(WIDTH, HEIGHT)` as an argument to define the
# dimensions of the window. The window will have a width of 700 pixels and a height of 700 pixels
# based on the values assigned to `WIDTH` and `HEIGHT` earlier in the code.
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# `pygame.display.set_caption("Planet Simulation")` is a function call in the Pygame library that sets
# the title or caption of the window where the graphics will be displayed. In this specific case, it
# sets the title of the window to "Planet Simulation". This title will be displayed at the top of the
# window frame when the program is executed, providing a descriptive label for the purpose of the
# simulation being run.
pygame.display.set_caption("Planet Simulation")

# These lines of code are defining color constants using RGB values for different objects in the
# planet simulation. Each color constant is represented as a tuple of three values corresponding to
# the red, green, and blue components of the color.
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
BROWN = (131.48, 86.585, 59.766)
DARK_BLUE = (2.3611, 28.333, 61.389)
GOLD = (241.05, 191.84, 45.823)

# `FONT = pygame.font.SysFont("comicsans", 20)` is a line of code in the Python script that is setting
# up a font for rendering text in the Pygame window.
FONT = pygame.font.SysFont("comicsans", 20)


# The `Planet` class in Python represents a celestial body with properties such as position, mass, and
# velocity, and includes methods for calculating gravitational attraction and updating its position
# based on interactions with other planets.
class Planet:

    # The lines of code you provided are defining constants and parameters used in the `Planet` class
    # for the planet simulation. Here is a breakdown of what each of these lines is doing:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU
    TIMESTEP = 3600 * 24

    def __init__(self, x, y, radius, color, mass):
        """
        This function initializes attributes for an object representing a celestial body in a
        simulation.
        
        :param x: The `x` parameter in the `__init__` method of your class seems to represent the
        x-coordinate of the object in a 2D space. It is used to initialize the x-coordinate of the
        object when an instance of the class is created
        :param y: The `y` parameter in the `__init__` method of your class seems to represent the
        initial y-coordinate of an object in a 2D space. It is used to define the position of the object
        along the vertical axis
        :param radius: The `radius` parameter in the `__init__` method of your class seems to represent
        the radius of an object. In the context of your code snippet, it appears to be used to define
        the size of the object, possibly for visualization or physics calculations
        :param color: Color is a parameter that represents the color of an object. It can be specified
        using various color models such as RGB (Red, Green, Blue), HEX (Hexadecimal), or named colors
        like 'red', 'blue', 'green', etc. The color parameter is used to define the visual appearance
        :param mass: The `mass` parameter in the `__init__` method of your class seems to represent the
        mass of an object. Mass is a measure of the amount of matter in an object. In physics, mass is
        typically measured in kilograms (kg) or grams (g). It plays a crucial role
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win, zoom_level, view_position):
        """
        The `draw` function in Python is responsible for rendering the orbit and details of a celestial
        body on the screen based on the provided parameters such as zoom level and view position.
        
        :param win: The `win` parameter in the `draw` method is typically the surface or window where
        you want to draw the objects. It is the surface on which you will be rendering the graphics,
        such as planets, orbits, and text in this case. This surface is usually created using a library
        like Py
        :param zoom_level: The `zoom_level` parameter in the `draw` method is used to determine the
        level of zoom applied to the drawing of the object. It is a factor by which the object's size
        and position are scaled to simulate zooming in or out of the scene. A higher `zoom_level` value
        :param view_position: The `view_position` parameter in the `draw` method represents the current
        position of the view or camera in the game world. It is used to determine where the objects
        should be drawn relative to the view position. By adjusting the view position, you can create
        the effect of moving the camera around the
        """
        x = (self.x * self.SCALE + WIDTH / 2 - view_position[0]) * zoom_level + view_position[0]
        y = (self.y * self.SCALE + HEIGHT / 2 - view_position[1]) * zoom_level + view_position[1]

        if len(self.orbit) > 2:
            update_points = []

            for point in self.orbit:
                x, y = point
                x = (x * self.SCALE + WIDTH / 2 - view_position[0]) * zoom_level + view_position[0]
                y = (y * self.SCALE + HEIGHT / 2 - view_position[1]) * zoom_level + view_position[1]
                update_points.append((x, y))

            pygame.draw.lines(win, self.color, False, update_points, 1)
        pygame.draw.circle(win, self.color, (int(x), int(y)), int(self.radius * zoom_level))

        if not self.sun:
            planet_names = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
            name_text = FONT.render(
                f"{planet_names[self.planet_index]}", 1, WHITE)

            distance_text = FONT.render(
                f" {round(self.distance_to_sun / 1000, 1)} km", 1, WHITE)
            win.blit(name_text, (x - name_text.get_width() /
                                 2, y - name_text.get_height() / 2 - 20))
            win.blit(distance_text, (x - distance_text.get_width() /
                                     2, y - distance_text.get_width() / 2))

    def set_planet_index(self, index):
        """
        This function sets the planet index for a given object.
        
        :param index: The `set_planet_index` method you provided is used to set the `planet_index`
        attribute of an object to the value passed as the `index` parameter
        """
        self.planet_index = index

    def attraction(self, other):
        """
        The function calculates the attraction force between two objects in a 2D space.
        
        :param other: The `other` parameter in the `attraction` method seems to represent another object
        in the system that interacts with the object calling the method. It likely has attributes such
        as `x`, `y`, `mass`, and `sun` that are used in the calculations within the method
        :return: The function `attraction` is returning the components of the gravitational force acting
        on the object `self` due to the presence of another object `other`. Specifically, it returns the
        horizontal component of the force (`force_x`) and the vertical component of the force
        (`force_y`).
        """
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets):
        """
        The `update_position` function calculates the total force exerted on a planet by other planets,
        updates its velocity and position accordingly, and appends the new position to its orbit.
        
        :param planets: The `planets` parameter in the `update_position` method is a list of all the
        other planets in the system. The method calculates the total gravitational force acting on the
        current planet (self) due to the gravitational attraction from all the other planets in the
        system. It then updates the velocity and
        """
        total_fx = total_fy = 0

        for planet in planets:

            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    """
    The main function initializes a simulation of the solar system with planets and their properties,
    allowing for user interaction to adjust the view and zoom level.
    """
    run = True
    clock = pygame.time.Clock()

    zoom_level = 1.0
    view_position = [0, 0]

    # planets and start
    # The code snippet you provided is initializing instances of the `Planet` class to represent
    # different planets in a solar system simulation. Here's a breakdown of what each part of the code
    # is doing:
    sun = Planet(0, 0, 40, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, 0, 1, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000
    mercury.set_planet_index(0)

    venus = Planet(0.723 * Planet.AU, 0, 2, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000
    venus.set_planet_index(1)

    earth = Planet(-1 * Planet.AU, 0, 3, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000
    earth.set_planet_index(2)

    mars = Planet(-1.524 * Planet.AU, 0, 1.5, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000
    mars.set_planet_index(3)

    jupiter = Planet(-5.203 * Planet.AU, 0, 7, BROWN, 1.898 * 10**27)
    jupiter.y_vel = -13.06 * 1000
    jupiter.set_planet_index(4)

    saturn = Planet(-9.582 * Planet.AU, 0, 5.5, GOLD, 5.683 * 10**26)
    saturn.y_vel = -9.68 * 1000
    saturn.set_planet_index(5)

    uranus = Planet(-19.22 * Planet.AU, 0, 4.5, DARK_BLUE, 8.681 * 10**25)
    uranus.y_vel = -6.81 * 1000
    uranus.set_planet_index(6)

    neptune = Planet(-30.05 * Planet.AU, 0, 4, BLUE, 1.024 * 10**26)
    neptune.y_vel = -5.43 * 1000
    neptune.set_planet_index(7)

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    # The code snippet you provided is the main game loop in a Pygame application. Here's a breakdown
    # of what each part of the loop is doing:
    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    view_position[1] += 50
                elif event.key == pygame.K_DOWN:
                    view_position[1] -= 50
                elif event.key == pygame.K_LEFT:
                    view_position[0] += 50
                elif event.key == pygame.K_RIGHT:
                    view_position[0] -= 50
                elif event.key == pygame.K_PLUS:
                    zoom_level *= 1.1
                elif event.key == pygame.K_MINUS:
                    zoom_level /= 1.1

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN, zoom_level, view_position)

        pygame.display.update()

    pygame.quit()


main()
