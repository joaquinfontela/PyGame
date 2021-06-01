from Config.configParser import CONFIGS
import pygame
import time
from Snake import Snake, CIRCLE_DIAMETER
from SnakeUtils.Direction.RightDirection import RightDirection
from SnakeUtils.Direction.LeftDirection import LeftDirection
from SnakeUtils.Direction.UpDirection import UpDirection
from SnakeUtils.Direction.DownDirection import DownDirection
from random import randrange
from TextFormatter.TextFormatter import TextFormatter

CIRCLE_RADIUS = CONFIGS["circle_diameter"]/2
FONT = CONFIGS["font"]
BACKGROUND_COLOR = CONFIGS["colors"]["background"]
SCORE_COLOR = CONFIGS["colors"]["score"]
NORMAL_FOOD_COLOR = CONFIGS["colors"]["normal_food"]
SPECIAL_FOOD_COLOR = CONFIGS["colors"]["special_food"]
SLEEP_PER_UPDATE = 1/CONFIGS["speed_diameters_per_second"]

PLAYER_LOST_SOUND_PATH = CONFIGS["sounds"]["player_lost"]
FOOD_COLLECTED_SOUND_PATH = CONFIGS["sounds"]["food_collected"]
SPECIAL_FOOD_COLLECTED_SOUND_PATH = CONFIGS["sounds"]["special_food_collected"]
pygame.mixer.init()
PLAYER_LOST_SOUND = pygame.mixer.Sound(PLAYER_LOST_SOUND_PATH)
FOOD_COLLECTED_SOUND = pygame.mixer.Sound(
    FOOD_COLLECTED_SOUND_PATH)
FOOD_COLLECTED_SOUND.set_volume(0.5)
SPECIAL_FOOD_COLLECTED_SOUND = pygame.mixer.Sound(
    SPECIAL_FOOD_COLLECTED_SOUND_PATH)
SPECIAL_FOOD_COLLECTED_SOUND.set_volume(0.5)


class Game:

    def __init__(self, window):
        pygame.mixer.init()
        self.window = window
        self.window.screen.fill(BACKGROUND_COLOR)
        self.moves = 0
        self.open = True
        self.score = 0
        self.snake = Snake(
            self.window, (int(CIRCLE_RADIUS * 21), int(CIRCLE_RADIUS * 21)))
        self._setRandomFoodPosition()
        self.specialFoodPosition = None
        self.specialFoodCountdown = 0
        pygame.display.update()
        while self.open:
            time.sleep(SLEEP_PER_UPDATE)
            self.moves += 1
            eventList = pygame.event.get()
            if pygame.QUIT in map(lambda e: e.type, eventList):
                self.open = False
                self.window.stopRunning()
            if eventList:
                event = eventList[0]
                if event.type == pygame.KEYDOWN:
                    self.handleKeyDown(event)
            self.updateSnakePosition()
            self.randomSpecialFoodSpawn()

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
            pygame.mixer.Sound.play(PLAYER_LOST_SOUND)
            self.open = False

    def _setRandomFoodPosition(self):
        self.foodPosition = self._getRandomFoodPosition()

    def _getRandomFoodPosition(self):
        screenWidth, screenHeight = self.window.getDimensions()
        foodPosition = (randrange(
            CIRCLE_RADIUS, screenWidth - CIRCLE_RADIUS, CIRCLE_RADIUS * 2), randrange(
            CIRCLE_RADIUS, screenHeight - CIRCLE_RADIUS, CIRCLE_RADIUS * 2))
        if list(foodPosition) in self.snake.getBodyPosition():
            return self._getRandomFoodPosition()
        return foodPosition

    def drawFood(self):
        pygame.draw.circle(self.window.screen, NORMAL_FOOD_COLOR,
                           self.foodPosition, CIRCLE_RADIUS)
        if self.specialFoodPosition:
            pygame.draw.circle(self.window.screen, SPECIAL_FOOD_COLOR,
                               self.specialFoodPosition, CIRCLE_RADIUS)

    def verifyCollisionWithFood(self):
        if list(self.foodPosition) in self.snake.getBodyPosition():
            self._setRandomFoodPosition()
            self.snake.eatFood()
            self.score += 10
            pygame.mixer.Sound.play(FOOD_COLLECTED_SOUND)
        if self.specialFoodPosition and list(self.specialFoodPosition) in self.snake.getBodyPosition():
            self.snake.eatFood()
            self.score += 50
            self.specialFoodPosition = None
            pygame.mixer.Sound.play(SPECIAL_FOOD_COLLECTED_SOUND)

    def _updateScore(self):
        scoreText = TextFormatter().formatText(
            f"Score: {self.score}", FONT, 60, SCORE_COLOR)
        self.window.screen.blit(
            scoreText, (150 - (scoreText.get_rect()[2]/2), 10))

    def randomSpecialFoodSpawn(self):
        self.specialFoodCountdown -= 1
        if self.specialFoodCountdown == 0:
            self.specialFoodPosition = None
        if self.moves % 250 == 0:
            self.specialFoodPosition = self._getRandomFoodPosition()
            self.specialFoodCountdown = 50
