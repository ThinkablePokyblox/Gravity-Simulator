# Imports
import pygame
import math
import random
pygame.init()
# Config
WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont("comicsans", 16)
pygame.display.set_caption("Planet Simulation")
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
WHITE = (255, 255, 255)
YELLOW = (255, 200, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
GREEN = (140, 255, 140)
BROWN = (153, 77, 0)
LIGHTBROWN = (255, 217, 179)
LIGHTBLUE = (102, 255, 255)
DARKBLUE = (13, 0, 77)
# Functions
def ConvertTime(Time):
    Unit = "Seconds"
    if Time >= 60:  # Minute
        Time /= 60
        Unit = "Minute"
        if Time >= 60:  # Hour
            Time /= 60
            Unit = "Hour"
            if Time >= 24:  # Day
                Time /= 24
                Unit = "Day"
                if Time >= 30:  # Month
                    Time /= 30
                    Unit = "Month"
                    if Time >= 12:  # Year
                        Time /= 12
                        Unit = "Year"
    return round(Time), Unit
# Classes
class Planet:

	AU = 146*10**9
	G = 6.67428e-11
	GameScale = 1 / AU
	TIMESTEP = 3600

	def __init__(self):
		self.x = 0
		self.y = 0
		self.radius = 0
		self.color = None
		self.mass = 0

		self.orbit = []
		self.distance_to_sun = 0
		self.PositionLocked = False

		self.x_vel = 0
		self.y_vel = 0

	def draw(self, win):
		x = self.x * Planet.GameScale + WIDTH / 2
		y = self.y * Planet.GameScale + HEIGHT / 2
		pygame.draw.circle(win, self.color, (x, y),(self.radius) * (Planet.GameScale))

	def attraction(self, other):
		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

		force = Planet.G * self.mass * other.mass / distance**2
		theta = math.atan2(distance_y, distance_x)
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force
		return force_x, force_y

	def update_position(self, planets):
		if self.PositionLocked == False:
			total_fx = total_fy = 0
			for planet in planets:
				if self == planet:
					continue

				fx, fy = self.attraction(planet)
				total_fx += fx
				total_fy += fy

			self.x_vel += total_fx / self.mass * Planet.TIMESTEP
			self.y_vel += total_fy / self.mass * Planet.TIMESTEP

			self.x += self.x_vel * Planet.TIMESTEP
			self.y += self.y_vel * Planet.TIMESTEP
			self.orbit.append((self.x, self.y))
class BackgroundStar:
	def __init__(self, radius, transparency, color, x, y) -> None:
		self.radius = radius
		self.transparency = transparency
		self.color = color
		self.x = x
		self.y = y
	
	def draw(self, win):
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
# Main
def main():
	run = True
	clock = pygame.time.Clock()

	planets = []
	backgroundStars = []

	for count in range(random.randrange(20,100)):
		Star = BackgroundStar(random.randrange(1,2), 1, WHITE, random.randrange(0, WIDTH), random.randrange(0, HEIGHT))
		backgroundStars.append(Star)
	
	mouseDown = False
	grow = False
	curentObject = None
	settingSpeed = False
	SpeedTimeUp = False
	SlowTimeDown = False

	scroll = 45461813.317888215

	while run:
		# Start
		clock.tick(60)
		WIN.fill((0, 0, 0))
		# FPS Text
		Fps = round(clock.get_fps())
		FpsText = ""
		if Fps >= 50:
			FpsText = FONT.render(f"{Fps} FPS", 1, GREEN)
		elif Fps >= 30 and Fps < 50:
			FpsText = FONT.render(f"{Fps} FPS", 1, YELLOW)
		elif Fps < 30:
			FpsText = FONT.render(f"{Fps} FPS", 1, RED)
		WIN.blit(FpsText, (0, 0))
		# Time Text
		Time = ConvertTime(Planet.TIMESTEP)
		TimeText = FONT.render(f"{Time[0]} {Time[1]}(s) Passes Every Second", 1, WHITE)
		WIN.blit(TimeText, (0, FpsText.get_height()))
        # Game Scale
		Planet.GameScale = scroll / Planet.AU
		# Collision Detection
		for planet in planets:
			for planet2 in planets:
				p1 = planet
				p2 = planet2

			if p1 == p2:
				continue

			distance = ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5
			if distance <= p1.radius + p2.radius:
				if p1.mass > p2.mass:
					planets.remove(p2)
					p1.mass += p2.mass
					p1.radius += p2.radius
				elif p2.mass > p1.mass:
					planets.remove(p1)
					p2.mass += p1.mass
					p2.radius += p1.radius
		# Events
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
				curentObject = Planet()
				curentObject.color = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
			elif event.type == pygame.MOUSEBUTTONUP:
				mouseDown = False
				settingSpeed = False
				grow = False
				if not curentObject.radius == 0:
					planets.append(curentObject)
					curentObject = None
            # Key Hold
			elif event.type == pygame.KEYDOWN:
                # Q
				if mouseDown == True and event.key == pygame.K_q:
					grow = True
                # E
				elif mouseDown == True and event.key == pygame.K_e:
					settingSpeed = True
				# L
				elif mouseDown == True and event.key == pygame.K_l:
					if curentObject.PositionLocked == True:
						curentObject.PositionLocked = False
					else:
						curentObject.PositionLocked = True
				# .
				elif mouseDown == False and event.key == pygame.K_PERIOD:
					if SlowTimeDown == False:
						SpeedTimeUp = True
				# ,
				elif mouseDown == False and event.key == pygame.K_COMMA:
					if SpeedTimeUp == False:
						SlowTimeDown = True
			elif event.type == pygame.KEYUP:
                # Q
				if mouseDown == True and event.key == pygame.K_q:
					grow = False
                # E
				elif mouseDown == True and event.key == pygame.K_e:
					settingSpeed = False
				# .
				elif mouseDown == False and event.key == pygame.K_PERIOD:
					if SlowTimeDown == False:
						SpeedTimeUp = False
				# ,
				elif mouseDown == False and event.key == pygame.K_COMMA:
					if SpeedTimeUp == False:
						SlowTimeDown = False
		# Time Control
		if SpeedTimeUp == True:
			ExactTimeText = FONT.render(f"{Planet.TIMESTEP} Seconds passes Every Second", 1, WHITE)
			WIN.blit(ExactTimeText, (0, TimeText.get_height() + FpsText.get_height()))
			Planet.TIMESTEP += 10
		elif SlowTimeDown == True:
			ExactTimeText = FONT.render(f"{Planet.TIMESTEP} Seconds passes Every Second", 1, WHITE)
			WIN.blit(ExactTimeText, (0, TimeText.get_height() + FpsText.get_height()))
			Planet.TIMESTEP -= 10
        # Object Creation
		if grow == True and settingSpeed == False and curentObject:
			mousePos = pygame.mouse.get_pos()
			curentObject.x = (mousePos[0] - WIDTH/2) * Planet.AU / scroll
			curentObject.y = (mousePos[1] - HEIGHT/2) * Planet.AU / scroll
			curentObject.radius += 100
			curentObject.mass += 1 * 10 ** 10
			curentObject.draw(WIN)
		elif grow == False and settingSpeed == False and curentObject:
			mousePos = pygame.mouse.get_pos()
			curentObject.x = (mousePos[0] - WIDTH/2) * Planet.AU / scroll
			curentObject.y = (mousePos[1] - HEIGHT/2) * Planet.AU / scroll
			curentObject.draw(WIN)
		elif grow == False and settingSpeed == True and curentObject:
			mousePos = pygame.mouse.get_pos()
			curentObject.x_vel = (((curentObject.x / Planet.AU * scroll) + WIDTH / 2) - mousePos[0]) / 1000
			curentObject.y_vel = (((curentObject.y / Planet.AU * scroll) + HEIGHT / 2) - mousePos[1]) / 1000
			curentObject.draw(WIN)
        # Making already existing objects
		for Star in backgroundStars:
			Star.draw(WIN)
		for planet in planets:
			planet.update_position(planets)
			planet.draw(WIN)
		# Update Display	
		pygame.display.update()
	# Quit
	pygame.quit()
main()