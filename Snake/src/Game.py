from Colors.Colors import BACKGROUND_MENU_COLOR as BACKGROUND_COLOR
from Colors.Colors import gray as GRAY, yellow as YELLOW
import pygame
import time
from Snake import Snake, CIRCLE_DIAMETER
from SnakeUtils.Direction.RightDirection import RightDirection
from SnakeUtils.Direction.LeftDirection import LeftDirection
from SnakeUtils.Direction.UpDirection import UpDirection
from SnakeUtils.Direction.DownDirection import DownDirection
from random import randrange
from TextFormatter.TextFormatter import TextFormatter

CIRCLE_RADIUS = CIRCLE_DIAMETER/2
FONT = "Fonts/retro.ttf"


class Game:

    def __init__(self, window):
        self.window = window
        self.window.screen.fill(BACKGROUND_COLOR)
        self.open = True
        self.score = 0
        self.snake = Snake(
            self.window, (int(CIRCLE_RADIUS * 21), int(CIRCLE_RADIUS * 21)))
        self._setRandomFoodPosition()
        pygame.display.update()
        while self.open:
            time.sleep(0.05)
            eventList = pygame.event.get()
            if pygame.QUIT in map(lambda e: e.type, eventList):
                self.open = False
                self.window.stopRunning()
            if eventList:
                event = eventList[0]
                if event.type == pygame.KEYDOWN:
                    self.handleKeyDown(event)
            self.updateSnakePosition()

    def handleKeyDown(self, event):
        if event.key == pygame.K_DOWN:
            self.snake.changeDirection(DownDirection())
        elif event.key == pygame.K_UP:
            self.snake.changeDirection(UpDirection())
        elif event.key == pygame.K_LEFT:
            self.snake.changeDirection(LeftDirection())
        elif event.key == pygame.K_RIGHT:
            self.snake.changeDirection(RightDirection())

    def updateSnakePosition(self):
        pygame.display.flip()
        self.snake.moveForward()
        self.verifyCollisionWithFood()
        self.window.screen.fill(BACKGROUND_COLOR)
        self._updateScore()
        self.drawFood()
        self.snake.draw()
        pygame.display.update()
        if self.snake.collisionWithMyself():
            self.open = False

    def _setRandomFoodPosition(self):
        screenWidth, screenHeight = self.window.getDimensions()
        self.foodPosition = (randrange(
            CIRCLE_RADIUS, screenWidth - CIRCLE_RADIUS, CIRCLE_RADIUS * 2), randrange(
            CIRCLE_RADIUS, screenHeight - CIRCLE_RADIUS, CIRCLE_RADIUS * 2))
        if list(self.foodPosition) in self.snake.getBodyPosition():
            self._setRandomFoodPosition()

    def drawFood(self):
        pygame.draw.circle(self.window.screen, YELLOW,
                           self.foodPosition, CIRCLE_RADIUS)

    def verifyCollisionWithFood(self):
        if list(self.foodPosition) in self.snake.getBodyPosition():
            self._setRandomFoodPosition()
            self.snake.eatFood()
            self.score += 10

    def _updateScore(self):
        scoreText = TextFormatter().formatText(
            f"Score: {self.score}", FONT, 60, GRAY)
        self.window.screen.blit(
            scoreText, (150 - (scoreText.get_rect()[2]/2), 10))
