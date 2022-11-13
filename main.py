# Imports #
import pygame
import math
import random
# Variables #
WINDOW_SIZE = (500, 500)
Objects = []
TIMESTEP = 0.01
# Color (RGB)
COLORS = [
    (255, 255, 255),
    (255, 200, 0),
    (100, 149, 237),
    (188, 39, 50),
    (80, 78, 81),
    (140, 255, 140),
    (153, 77, 0),
    (255, 217, 179),
    (102, 255, 255),
    (13, 0, 77)
]
# Functions #
def ConvertTime(Time):
    Unit = "Seconds"
    if Time >= 60: # Minute
        Time /= 60
        Unit = "Minute"
        if Time >= 60: # Hour
            Time /= 60
            Unit = "Hour"
            if Time >= 24: # Day
                Time /= 24
                Unit = "Day"
                if Time >= 30: # Month
                    Time /= 30
                    Unit = "Month"
                    if Time >= 12: # Year
                        Time /= 12
                        Unit = "Year"
    return round(Time), Unit
# Main #
pygame.init()
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
FONT = pygame.font.SysFont("comicsans", 16)
pygame.display.set_caption("Planet Simulation")
#
class object:

    AU = 146*10**9
    G = 6.67428e-11
    GameScale = 1 / AU
    TIMESTEP = 160

    def __init__(self):
        self.mass = 0
        self.radius = 0
        self.x = 0
        self.y = 0
        self.xVelocity = 0
        self.yVelocity = 0
        self.color = None

    def draw(self, win):
        x = self.x
        y = self.y
        pygame.draw.circle(win, self.color, (x, y),(self.radius) * object.GameScale)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        force = object.G * self.mass * other.mass / distance**2
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

        self.xVelocity += total_fx / self.mass * object.TIMESTEP
        self.yVelocity += total_fy / self.mass * object.TIMESTEP
        self.x += self.xVelocity * object.TIMESTEP
        self.y += self.yVelocity * object.TIMESTEP


def startGame():
    run = True
    clock = pygame.time.Clock()

    mouseDown = False
    grow = False
    curentObject = None
    settingSpeed = False
    scroll = 1

    while run:
        WINDOW.fill((0, 0, 0))
        clock.tick(60)

        Fps = round(clock.get_fps())
        FpsText = ""
        if Fps >= 50:
            FpsText = FONT.render(f"{Fps} FPS", 1, (140,255,140))
        elif Fps >= 30 and Fps < 50:
            FpsText = FONT.render(f"{Fps} FPS", 1, (255, 200, 0))
        elif Fps < 30:
            FpsText = FONT.render(f"{Fps} FPS", 1, (188, 39, 50))
        WINDOW.blit(FpsText, (0,0))
		
        Time = ConvertTime(object.TIMESTEP)
        TimeText = FONT.render(f"{Time[0]} {Time[1]}(s) Passes Every Second", 1, (255,255,255))
        WINDOW.blit(TimeText, (0,FpsText.get_height()))

        object.GameScale = scroll / object.AU

        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                run = False
            # Mouse Hold
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll *= 1.1
                elif event.button == 5:
                    scroll /= 1.1
                mouseDown = True
                curentObject = object()
                curentObject.color = COLORS[random.randrange(0, len(COLORS))]
            elif event.type == pygame.MOUSEBUTTONUP:
                mouseDown = False
                settingSpeed = False
                grow = False
                if not curentObject.radius == 0:
                    Objects.append(curentObject)
                    curentObject = None
            # Key Hold
            elif event.type == pygame.KEYDOWN:
                # Q
                if mouseDown == True and event.key == pygame.K_q:
                    grow = True
                # E
                elif mouseDown == True and event.key == pygame.K_e:
                    settingSpeed = True
            elif event.type == pygame.KEYUP:
                # Q
                if mouseDown == True and event.key == pygame.K_q:
                    grow = False
                # E
                elif mouseDown == True and event.key == pygame.K_e:
                    settingSpeed = False
            # End
        # Object Creation
        if grow == True and settingSpeed == False and curentObject:
            mousePos = pygame.mouse.get_pos()
            curentObject.x = mousePos[0] 
            curentObject.y = mousePos[1] 
            curentObject.radius = curentObject.radius + (0.5 / object.GameScale)
            curentObject.mass = curentObject.mass + 1000000
            curentObject.draw(WINDOW)
        elif grow == False and settingSpeed == False and curentObject:
            mousePos = pygame.mouse.get_pos()
            curentObject.x = mousePos[0]
            curentObject.y = mousePos[1]
            curentObject.draw(WINDOW)
        elif grow == False and settingSpeed == True and curentObject:
            mousePos = pygame.mouse.get_pos()
            curentObject.xVelocity = (curentObject.x - mousePos[0]) / 1000
            curentObject.yVelocity = (curentObject.y - mousePos[1]) / 1000
            print(curentObject.xVelocity)
            print(curentObject.yVelocity)
            curentObject.draw(WINDOW)
        # Making already existing objects
        for Object in Objects:
            Object.update_position(Objects)
            Object.draw(WINDOW)

        pygame.display.update()

startGame()