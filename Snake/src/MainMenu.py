import pygame
from pygame.constants import KEYUP
from TextFormatter.TextFormatter import TextFormatter
from Config.configParser import CONFIGS
import Game
import SettingsMenu
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


class MainMenu:

    def __init__(self, window):
        self.window = window
        self.open = True
        self.buttonSelected = 1
        self._displayTexts()
        self._loop()

    def _displayTexts(self):
        '''
        Displays the text in the main menu.
        '''
        self.window.screen.fill(BACKGROUND_COLOR)
        title = TextFormatter().formatText("PySnake", FONT, 150, LOGO_COLOR)
        playButton = TextFormatter().formatText(
            "PLAY", FONT, 100, SELECTED_COLOR if self.buttonSelected % 3 == 1 else NON_SELECTED_COLOR)
        settingsButton = TextFormatter().formatText(
            "SETTINGS", FONT, 100, SELECTED_COLOR if self.buttonSelected % 3 == 2 else NON_SELECTED_COLOR)
        quitButton = TextFormatter().formatText(
            "QUIT", FONT, 100, SELECTED_COLOR if self.buttonSelected % 3 == 0 else NON_SELECTED_COLOR)
        screenWidth, _ = self.window.getDimensions()
        self.window.screen.blit(
            title, (screenWidth/2 - (title.get_rect()[2]/2), 80))
        self.window.screen.blit(
            playButton, (screenWidth/2 - (playButton.get_rect()[2]/2), 325))
        self.window.screen.blit(
            settingsButton, (screenWidth/2 - (settingsButton.get_rect()[2]/2), 450))
        self.window.screen.blit(
            quitButton, (screenWidth/2 - (quitButton.get_rect()[2]/2), 575))
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
                    if event.key in (pygame.K_DOWN, pygame.K_UP):
                        self._switchPlaySelected(event.key)
                        self._displayTexts()
                    if event.key == pygame.K_RETURN:
                        if self.buttonSelected % 3 == 1:
                            pygame.mixer.Sound.play(
                                SELECT_START_GAME_SOUND)
                            Game.Game(self.window, 2)
                        elif self.buttonSelected % 3 == 2:
                            pygame.mixer.Sound.play(
                                SELECT_OPTION_SOUND)
                            SettingsMenu.SettingsMenu(self.window)
                if event.type == pygame.QUIT or \
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.buttonSelected % 3 == 0):
                    pygame.mixer.Sound.play(SELECT_OPTION_SOUND)
                    time.sleep(0.2)
                    self.open = False
                    self.window.stopRunning()

    def _switchPlaySelected(self, eventKey):
        pygame.mixer.Sound.play(CHANGE_SELECTED_OPTION_SOUND)
        if eventKey == pygame.K_DOWN:
            self.buttonSelected += 1
        else:
            self.buttonSelected -= 1
