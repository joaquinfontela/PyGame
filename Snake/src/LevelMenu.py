import pygame
from TextFormatter.TextFormatter import TextFormatter
from Config.configParser import CONFIGS
import Game
import time

THEME = CONFIGS["current_theme"]
BACKGROUND_COLOR = CONFIGS["colors"][THEME]["background"]
LOGO_COLOR = CONFIGS["colors"][THEME]["logo"]
SELECTED_COLOR = CONFIGS["colors"][THEME]["selected_option"]
NON_SELECTED_COLOR = CONFIGS["colors"][THEME]["non_selected_option"]
FONT = "Fonts/retro.ttf"

CHANGE_SELECTED_OPTION_SOUND_PATH = CONFIGS["sounds"]["change_selected_option"]
SELECT_OPTION_SOUND_PATH = CONFIGS["sounds"]["select_option"]
SELECT_START_GAME_SOUND_PATH = CONFIGS["sounds"]["select_start_game"]
pygame.mixer.init()
CHANGE_SELECTED_OPTION_SOUND = pygame.mixer.Sound(
    CHANGE_SELECTED_OPTION_SOUND_PATH)
CHANGE_SELECTED_OPTION_SOUND.set_volume(0.5)
SELECT_OPTION_SOUND = pygame.mixer.Sound(
    SELECT_OPTION_SOUND_PATH)
SELECT_OPTION_SOUND.set_volume(0.5)
SELECT_START_GAME_SOUND = pygame.mixer.Sound(
    SELECT_START_GAME_SOUND_PATH)
SELECT_START_GAME_SOUND.set_volume(0.5)


class LevelMenu:

    def __init__(self, window):
        self.window = window
        self.open = True
        self.buttonSelected = 1
        self._displayTexts()
        self._loop()

    def _displayTexts(self):
        self.window.screen.fill(BACKGROUND_COLOR)
        title = TextFormatter().formatText("SELECT LEVEL:", FONT, 150, LOGO_COLOR)
        level1Title = TextFormatter().formatText("1", FONT, 100,
                                                 SELECTED_COLOR if self.buttonSelected % 5 == 1 else NON_SELECTED_COLOR)
        level2Title = TextFormatter().formatText("2", FONT, 100,
                                                 SELECTED_COLOR if self.buttonSelected % 5 == 2 else NON_SELECTED_COLOR)
        level3Title = TextFormatter().formatText("3", FONT, 100,
                                                 SELECTED_COLOR if self.buttonSelected % 5 == 3 else NON_SELECTED_COLOR)
        level4Title = TextFormatter().formatText("4", FONT, 100,
                                                 SELECTED_COLOR if self.buttonSelected % 5 == 4 else NON_SELECTED_COLOR)
        level5Title = TextFormatter().formatText("5", FONT, 100,
                                                 SELECTED_COLOR if self.buttonSelected % 5 == 0 else NON_SELECTED_COLOR)
        screenWidth, _ = self.window.getDimensions()
        self.window.screen.blit(
            title, (screenWidth/2 - (title.get_rect()[2]/2), 80))
        self.window.screen.blit(
            level1Title, (screenWidth/6, 400))
        self.window.screen.blit(
            level2Title, (2 * screenWidth/6, 400))
        self.window.screen.blit(
            level3Title, (3 * screenWidth/6, 400))
        self.window.screen.blit(
            level4Title, (4 * screenWidth/6, 400))
        self.window.screen.blit(
            level5Title, (5 * screenWidth/6, 400))
        pygame.display.update()

    def _loop(self):
        '''
        Executes the main loop of the main menu,
        which is in charge of identifying which option is selected
        and updating the information graphically in the correct moment.
        '''
        while self.open:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        self._changeLevelSelected(event.key)
                        self._displayTexts()
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.Sound.play(
                            SELECT_START_GAME_SOUND)
                        level = self.buttonSelected % 5
                        Game.Game(self.window, level if level > 0 else 5)
                if event.type == pygame.QUIT or \
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.buttonSelected % 3 == 0):
                    pygame.mixer.Sound.play(SELECT_OPTION_SOUND)
                    time.sleep(0.2)
                    self.open = False
                    self.window.stopRunning()

    def _changeLevelSelected(self, eventKey):
        pygame.mixer.Sound.play(CHANGE_SELECTED_OPTION_SOUND)
        if eventKey == pygame.K_LEFT:
            self.buttonSelected -= 1
        else:
            self.buttonSelected += 1
