from SnakeUtils.Direction.Direction import Direction
import pygame
from Config.configParser import CONFIGS
from SnakeUtils.Direction.RightDirection import RightDirection

CIRCLE_DIAMETER = CONFIGS["circle_diameter"]
SNAKE_COLOR = CONFIGS["colors"]["snake"]


class Snake:

    def __init__(self, window, pos):
        self.window = window
        self.body = [[pos[0], pos[1]], [pos[0] - CIRCLE_DIAMETER, pos[1]],
                     [pos[0] - 2 * CIRCLE_DIAMETER, pos[1]
                      ], [pos[0] - 3 * CIRCLE_DIAMETER, pos[1]],
                     [pos[0] - 4 * CIRCLE_DIAMETER, pos[1]]]
        self.direction = Direction(self.window, RightDirection())

    def moveForward(self):
        self.body = self.direction.move(self.body, CIRCLE_DIAMETER)

    def draw(self):
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
        positionsOfBody = {tuple(pos): self.body.count(pos)
                           for pos in self.body}
        return len(list(filter(lambda x: x > 1, positionsOfBody.values()))) > 0
