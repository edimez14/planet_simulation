import pygame
import math
pygame.init()

WIDTH, HEIGHT = 700, 700

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
BROWN = (131.48, 86.585, 59.766)
DARK_BLUE = (2.3611, 28.333, 61.389)
GOLD = (241.05, 191.84, 45.823)

FONT = pygame.font.SysFont("comicsans", 20)


class Planet:

    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU
    TIMESTEP = 3600 * 24

    def __init__(self, x, y, radius, color, mass):
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
        self.planet_index = index

    def attraction(self, other):
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
    run = True
    clock = pygame.time.Clock()

    zoom_level = 1.0
    view_position = [0, 0]

    # planets and start
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
