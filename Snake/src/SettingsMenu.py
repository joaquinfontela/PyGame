from Config.configParser import CONFIGS
from TextFormatter.TextFormatter import TextFormatter
import pygame
import time

THEME = CONFIGS["current_theme"]
BACKGROUND_COLOR = CONFIGS["colors"][THEME]["background"]
LOGO_COLOR = CONFIGS["colors"][THEME]["logo"]
SELECTED_COLOR = CONFIGS["colors"][THEME]["selected_option"]
NON_SELECTED_COLOR = CONFIGS["colors"][THEME]["non_selected_option"]
FONT = "Fonts/retro.ttf"

THEME_DICT = {"classic": "CLASSIC",
              "black_and_white": "B&w",
              "white_and_black": "W&B",
              "fire": "FIRE",
              "oceanic": "OCEANIC"}

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


class SettingsMenu:

    def __init__(self, window):
        self.window = window
        self.open = True
        self.themeTitleSelected = True
        self._displayText()
        self._loop()

    def _displayText(self):
        self.window.screen.fill(BACKGROUND_COLOR)
        title = TextFormatter().formatText("SETTINGS", FONT, 150, LOGO_COLOR)
        themeTitle = TextFormatter().formatText("COLOR THEME", FONT, 75,
                                                SELECTED_COLOR if self.themeTitleSelected else NON_SELECTED_COLOR)
        speedTitle = TextFormatter().formatText("SNAKE SPEED", FONT, 75,
                                                SELECTED_COLOR if not self.themeTitleSelected else NON_SELECTED_COLOR)
        themeSwitch = TextFormatter().formatText(
            THEME_DICT[CONFIGS["current_theme"]], FONT, 75, NON_SELECTED_COLOR)
        speedSwitch = TextFormatter().formatText(
            str(CONFIGS["speed_diameters_per_second"]), FONT, 75, NON_SELECTED_COLOR)
        screenWidth, _ = self.window.getDimensions()
        self.window.screen.blit(
            title, (screenWidth/2 - (title.get_rect()[2]/2), 80))
        self.window.screen.blit(
            themeTitle, (screenWidth/2 - (themeTitle.get_rect()[2]/2) - screenWidth/4, 350))
        self.window.screen.blit(
            speedTitle, (screenWidth/2 - (speedTitle.get_rect()[2]/2) - screenWidth/4, 500))
        self.window.screen.blit(
            themeSwitch, (screenWidth/2 - (themeSwitch.get_rect()[2]/2) + screenWidth/4, 350))
        self.window.screen.blit(
            speedSwitch, (screenWidth/2 - (speedSwitch.get_rect()[2]/2) + screenWidth/4, 500))
        pygame.display.update()

    def _loop(self):
        while self.open:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_DOWN, pygame.K_UP):
                        self._switchPlaySelected(event.key)
                        self._displayTexts()
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.Sound.play(SELECT_START_GAME_SOUND)
                        if self.buttonSelected % 3 == 1:
                            Game.Game(self.window)
                        elif self.buttonSelected % 3 == 2:
                            SettingsMenu.SettingsMenu(self.window)
                if event.type == pygame.QUIT:
                    pygame.mixer.Sound.play(SELECT_OPTION_SOUND)
                    time.sleep(0.2)
                    self.open = False
                    self.window.stopRunning()
