from Config.configParser import CONFIGS
import pygame
import time
from random import randint
from Snake import Snake, CIRCLE_DIAMETER
from SnakeUtils.Direction.RightDirection import RightDirection
from SnakeUtils.Direction.LeftDirection import LeftDirection
from SnakeUtils.Direction.UpDirection import UpDirection
from SnakeUtils.Direction.DownDirection import DownDirection
from random import randrange
from TextFormatter.TextFormatter import TextFormatter
from LevelConfiguration import LevelConfiguration
import MainMenu
from data.ScoresManager import ScoresManager

CIRCLE_RADIUS = CONFIGS["circle_diameter"]/2
FONT = CONFIGS["font"]

THEME = CONFIGS["current_theme"]
BACKGROUND_COLOR = CONFIGS["colors"][THEME]["background"]
SCORE_COLOR = CONFIGS["colors"][THEME]["score"]
NORMAL_FOOD_COLOR = CONFIGS["colors"][THEME]["normal_food"]
SPECIAL_FOOD_COLOR = CONFIGS["colors"][THEME]["special_food"]
WALL_COLOR = CONFIGS["colors"][THEME]["walls"]
SLEEP_PER_UPDATE = 1/CONFIGS["speed_diameters_per_second"]

PLAYER_LOST_SOUND_PATH = CONFIGS["sounds"]["player_lost"]
FOOD_COLLECTED_SOUND_PATH = CONFIGS["sounds"]["food_collected"]
SPECIAL_FOOD_COLLECTED_SOUND_PATH = CONFIGS["sounds"]["special_food_collected"]
GAME_MUSIC = CONFIGS["sounds"]["game_music"]
pygame.mixer.init()
PLAYER_LOST_SOUND = pygame.mixer.Sound(PLAYER_LOST_SOUND_PATH)
PLAYER_LOST_SOUND.set_volume(0.5)
FOOD_COLLECTED_SOUND = pygame.mixer.Sound(
    FOOD_COLLECTED_SOUND_PATH)
FOOD_COLLECTED_SOUND.set_volume(0.5)
SPECIAL_FOOD_COLLECTED_SOUND = pygame.mixer.Sound(
    SPECIAL_FOOD_COLLECTED_SOUND_PATH)
SPECIAL_FOOD_COLLECTED_SOUND.set_volume(0.5)

ARROW_KEYS = (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT)


class Game:

    def __init__(self, window, level):
        '''
        Initializes the main loop of the game.
        '''
        pygame.mixer.init()
        self.window = window
        self.level = level
        self.walls = LevelConfiguration(
            self.window, self.level).getLevelWalls()
        self.window.screen.fill(BACKGROUND_COLOR)
        self.moves = 0
        self.open = True
        self.score = 0
        self.snake = Snake(
            self.window, LevelConfiguration(self.window, self.level).getInitialPosAndDirection(), self.walls)
        self._setRandomFoodPosition()
        self.changedDirection = False
        self.pendingEvents = []
        self.specialFoodPosition = None
        self.specialFoodCountdown = 0
        pygame.display.update()
        pygame.mixer.music.load(GAME_MUSIC[self.level - 1])
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        while self.open:
            time.sleep(SLEEP_PER_UPDATE)
            self.moves += 1
            self.changedDirection = False
            self._postPendingEvents()
            eventList = pygame.event.get()
            for event in eventList:
                self.changedDirection = False
                if event.type == pygame.QUIT:
                    self.open = False
                    self.window.stopRunning()
                if event.type == pygame.KEYUP and event.key in ARROW_KEYS:
                    self.handleKeyUp(event)
                    self.randomSpecialFoodSpawn()
                    self._savePendingEvents(event, eventList)
                    break
            if not self.changedDirection:
                self.updateSnakePosition()
                self.randomSpecialFoodSpawn()

    def _postPendingEvents(self):
        for e in self.pendingEvents:
            pygame.event.post(e)

    def _savePendingEvents(self, lastEventProcessed, eventList):
        lastEventProcessedIdx = eventList.index(lastEventProcessed)
        self.pendingEvents = eventList[lastEventProcessedIdx + 1:]

    def handleKeyUp(self, event):
        '''
        Handles the event when a key is pressed.
        It ignores the event if the key pressed is not one of the four arrows.
        '''
        if event.key == pygame.K_DOWN:
            self.snake.changeDirection(DownDirection())
        elif event.key == pygame.K_UP:
            self.snake.changeDirection(UpDirection())
        elif event.key == pygame.K_LEFT:
            self.snake.changeDirection(LeftDirection())
        elif event.key == pygame.K_RIGHT:
            self.snake.changeDirection(RightDirection())
        self.changedDirection = True
        self.updateSnakePosition()

    def updateSnakePosition(self):
        '''
        Updates the position of the snake logically and graphically.
        '''
        pygame.display.flip()
        self.snake.moveForward()
        self.verifyCollisionWithFood()
        self.window.screen.fill(BACKGROUND_COLOR)
        self.drawFood()
        self.snake.draw()
        self.drawWalls()
        self._updateScore()
        pygame.display.update()
        if self.snake.collisionWithMyself() or self.snake.collisionWithWalls():
            pygame.mixer.Sound.play(PLAYER_LOST_SOUND)
            pygame.mixer.music.stop()
            self.open = False
            ScoresManager().save(
                f"random_id{randint(10000, 99999)}", self.score, self.level)
            MainMenu.MainMenu(self.window)

    def _setRandomFoodPosition(self):
        '''
        Sets a random new position for the food.
        '''
        self.foodPosition = self._getRandomFoodPosition()

    def _getRandomFoodPosition(self):
        '''
        Returns a random position for food in the map.
        If the player is in that position, it is calculated again.
        '''
        screenWidth, screenHeight = self.window.getDimensions()
        foodPosition = (randrange(
            CIRCLE_RADIUS, screenWidth - CIRCLE_RADIUS, CIRCLE_RADIUS * 2), randrange(
            CIRCLE_RADIUS, screenHeight - CIRCLE_RADIUS, CIRCLE_RADIUS * 2))
        if list(foodPosition) in self.snake.getBodyPosition() or list(foodPosition) in self.walls:
            return self._getRandomFoodPosition()
        return foodPosition

    def drawWalls(self):
        for wall in self.walls:
            x, y = wall
            pygame.draw.circle(self.window.screen,
                               WALL_COLOR, (x, y), CIRCLE_RADIUS)

    def drawFood(self):
        '''
        Draws food and special food if it applies.
        '''
        pygame.draw.circle(self.window.screen, NORMAL_FOOD_COLOR,
                           self.foodPosition, CIRCLE_RADIUS)
        if self.specialFoodPosition:
            pygame.draw.circle(self.window.screen, SPECIAL_FOOD_COLOR,
                               self.specialFoodPosition, CIRCLE_RADIUS)

    def verifyCollisionWithFood(self):
        '''
        Verifies if the snake has eaten the food and scores the corresponding points,
        it also randoms a new food position.
        '''
        if list(self.foodPosition) in self.snake.getBodyPosition():
            self._setRandomFoodPosition()
            self.snake.eatFood()
            self.score += 10
            pygame.mixer.Sound.play(FOOD_COLLECTED_SOUND)
        if self.specialFoodPosition and list(self.specialFoodPosition) in self.snake.getBodyPosition():
            self.snake.eatFood()
            self.score += (50 + self.specialFoodCountdown * 2)
            self.specialFoodPosition = None
            pygame.mixer.Sound.play(SPECIAL_FOOD_COLLECTED_SOUND)

    def _updateScore(self):
        '''
        Updates graphically the current score of the player.
        '''
        scoreText = TextFormatter().formatText(
            f"Score: {self.score}", FONT, 60, SCORE_COLOR, 150)
        self.window.screen.blit(
            scoreText, (150 - (scoreText.get_rect()[2]/2), 10))

    def randomSpecialFoodSpawn(self):
        '''
        Takes care of the special food spawn logic: how much time left for it to disappear, 
        and when to randomize its appearance.
        '''
        self.specialFoodCountdown -= 1
        if self.specialFoodCountdown == 0:
            self.specialFoodPosition = None
        if self.moves % 250 == 0:
            self.specialFoodPosition = self._getRandomFoodPosition()
            self.specialFoodCountdown = 25
        if self.specialFoodPosition:
            countdown = TextFormatter().formatText(str(self.specialFoodCountdown),
                                                   FONT, 70, SPECIAL_FOOD_COLOR)
            self.window.screen.blit(
                countdown, (self.window.getDimensions()[0] - 100, 10))
            pygame.display.update()
