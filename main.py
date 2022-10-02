# Imports #
import pygame
import math
# Variables #
WINDOW_SIZE = (500, 500)
Objects = []
COLORS = [
    (255,255,255)
]
# Main #
pygame.init()
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
FONT = pygame.font.SysFont("comicsans", 16)
pygame.display.set_caption("Planet Simulation")

class object:
    def __init__(self):
        self.mass = 0
        self.radius = 0
        self.x = 0
        self.y = 0
        self.xVelocity = 0
        self.yVelocity = 0
    def draw(self):
        pygame.draw.circle(WINDOW,(255,0,0),(self.x,self.y),self.radius)

def startGame():
    run = True

    mouseDown = False
    grow = False
    curentObject = None
    CalculateSpeed = False

    while run:
        WINDOW.fill((0,0,0))
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                run = False
            # Mouse Hold
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
                curentObject = object()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouseDown = False
                Objects.append(curentObject)
                curentObject = None
            # Key Hold
            elif event.type == pygame.KEYDOWN:
                # Q
                if mouseDown == True and event.key == pygame.K_q:
                    grow = True
                # W
                elif mouseDown == True and event.key == pygame.K_w:
                    CalculateSpeed = True
            elif event.type == pygame.KEYUP:
                # Q
                if mouseDown == True and event.key == pygame.K_q:
                    grow = False
                # W
                elif mouseDown == True and event.key == pygame.K_w:
                    CalculateSpeed = True
            # End
        if grow:
            mousePos = pygame.mouse.get_pos()
            curentObject.x = mousePos[0]
            curentObject.y = mousePos[1]
            curentObject.radius = curentObject.radius + 0.1
            curentObject.draw()
        elif not grow and curentObject:
            curentObject.draw()
        elif not grow and CalculateSpeed:
            pass
        for Object in Objects:
            Object.draw()
        
        pygame.display.update()
        
startGame()