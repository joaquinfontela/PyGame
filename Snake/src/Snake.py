import pygame
from Config.configParser import CONFIGS

CIRCLE_DIAMETER = CONFIGS["circle_diameter"]

THEME = CONFIGS["current_theme"]
SNAKE_COLOR = CONFIGS["colors"][THEME]["snake"]


class Snake:

    def __init__(self, window, pos, walls):
        self.window = window
        bodyPos = pos[0]
        direction = pos[1]
        self.body = bodyPos
        self.direction = direction
        self.mapWalls = walls

    def moveForward(self):
        '''
        Moves the snake one step in the direction it was moving.
        '''
        self.body = self.direction.move(self.body, CIRCLE_DIAMETER)

    def draw(self):
        '''
        Draws the snake in the window of the game.
        '''
        for pos in self.body:
            pygame.draw.circle(self.window.screen, SNAKE_COLOR,
                               (pos[0], pos[1]), CIRCLE_DIAMETER/2)
        screenWidth, screenHeight = self.window.getDimensions()
        self.body = [[pos[0] if pos[0] >= 0 else screenWidth + pos[0],
                     pos[1] if pos[1] >= 0 else screenHeight + pos[1]]
                     for pos in self.body]
        self.body = [[pos[0] if pos[0] <= screenWidth else pos[0] - screenWidth,
                      pos[1] if pos[1] <= screenHeight else pos[1] - screenHeight]
                     for pos in self.body]

    def changeDirection(self, newDirection):
        self.direction.changeState(newDirection)

    def getBodyPosition(self):
        return self.body

    def eatFood(self):
        self.body.append(self.direction.getLastPoppedBodyPosition())

    def collisionWithMyself(self):
        '''
        Returns a boolean indicating if the snake is having a collision with itself.
        '''
        positionsOfBody = {tuple(pos): self.body.count(pos)
                           for pos in self.body}
        return len(list(filter(lambda x: x > 1, positionsOfBody.values()))) > 0

    def collisionWithWalls(self):
        for posBody in self.body:
            if posBody in self.mapWalls:
                return True
        return False
