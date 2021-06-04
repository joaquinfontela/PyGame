import MainMenu
from Config.configParser import CONFIGS, updateColorTheme, updateSpeed
from TextFormatter.TextFormatter import TextFormatter
import pygame
import time
import os
import sys

THEME = CONFIGS["current_theme"]
BACKGROUND_COLOR = CONFIGS["colors"][THEME]["background"]
LOGO_COLOR = CONFIGS["colors"][THEME]["logo"]
SELECTED_COLOR = CONFIGS["colors"][THEME]["selected_option"]
NON_SELECTED_COLOR = CONFIGS["colors"][THEME]["non_selected_option"]
FONT = "Fonts/retro.ttf"

THEME_DICT = {
    "classic": "CLASSIC",
    "black_and_white": "B&w",
    "white_and_black": "W&B",
    "fire": "FIRE",
    "oceanic": "OCEANIC",
}

SPEED_OPTIONS = [5, 10, 15]

CHANGE_SELECTED_OPTION_SOUND_PATH = CONFIGS["sounds"]["change_selected_option"]
SELECT_OPTION_SOUND_PATH = CONFIGS["sounds"]["select_option"]
SELECT_START_GAME_SOUND_PATH = CONFIGS["sounds"]["select_start_game"]
pygame.mixer.init()
CHANGE_SELECTED_OPTION_SOUND = pygame.mixer.Sound(CHANGE_SELECTED_OPTION_SOUND_PATH)
CHANGE_SELECTED_OPTION_SOUND.set_volume(0.5)
SELECT_OPTION_SOUND = pygame.mixer.Sound(SELECT_OPTION_SOUND_PATH)
SELECT_OPTION_SOUND.set_volume(0.5)


class SettingsMenu:
    def __init__(self, window):
        self.window = window
        self.open = True
        self.themeTitleSelected = True
        self.showInstructions = True
        self._displayTexts()
        self._loop()

    def _displayTexts(self):
        self.window.screen.fill(BACKGROUND_COLOR)
        title = TextFormatter().formatText("SETTINGS", FONT, 150, LOGO_COLOR)
        themeTitle = TextFormatter().formatText(
            "COLOR THEME",
            FONT,
            75,
            SELECTED_COLOR if self.themeTitleSelected else NON_SELECTED_COLOR,
        )
        speedTitle = TextFormatter().formatText(
            "SNAKE SPEED",
            FONT,
            75,
            SELECTED_COLOR if not self.themeTitleSelected else NON_SELECTED_COLOR,
        )
        instructions = TextFormatter().formatText(
            "PRESS 'S' TO SAVE. PRESS 'Q' TO GO TO THE MAIN MENU."
            if self.showInstructions
            else "CHANGES SAVED. REBOOT THE GAME FOR UPDATE.",
            FONT,
            35,
            LOGO_COLOR,
        )
        themeSwitch = TextFormatter().formatText(
            THEME_DICT[CONFIGS["current_theme"]], FONT, 75, NON_SELECTED_COLOR
        )
        speedSwitch = TextFormatter().formatText(
            str(CONFIGS["speed_diameters_per_second"]), FONT, 75, NON_SELECTED_COLOR
        )
        screenWidth, _ = self.window.getDimensions()
        self.window.screen.blit(
            title, (screenWidth / 2 - (title.get_rect()[2] / 2), 80)
        )
        self.window.screen.blit(
            themeTitle,
            (screenWidth / 2 - (themeTitle.get_rect()[2] / 2) - screenWidth / 4, 350),
        )
        self.window.screen.blit(
            speedTitle,
            (screenWidth / 2 - (speedTitle.get_rect()[2] / 2) - screenWidth / 4, 500),
        )
        self.window.screen.blit(
            themeSwitch,
            (screenWidth / 2 - (themeSwitch.get_rect()[2] / 2) + screenWidth / 4, 350),
        )
        self.window.screen.blit(
            speedSwitch,
            (screenWidth / 2 - (speedSwitch.get_rect()[2] / 2) + screenWidth / 4, 500),
        )
        self.window.screen.blit(
            instructions, (screenWidth / 2 - (instructions.get_rect()[2] / 2), 650)
        )
        pygame.display.update()

    def _loop(self):
        while self.open:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_DOWN, pygame.K_UP):
                        self._switchThemeTitleSelected()
                        self._displayTexts()
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        self._handleSettingsChange(event.key)
                        self._displayTexts()
                    if event.key == pygame.K_s:
                        self._handleSave()
                        # os.execv(sys.executable, ["python", __file__, *sys.argv[1:]])
                    if event.key == pygame.K_q:
                        MainMenu.MainMenu(self.window)
                if event.type == pygame.QUIT:
                    pygame.mixer.Sound.play(SELECT_OPTION_SOUND)
                    time.sleep(0.2)
                    self.open = False
                    self.window.stopRunning()

    def _switchThemeTitleSelected(self):
        self.themeTitleSelected = not self.themeTitleSelected
        pygame.mixer.Sound.play(CHANGE_SELECTED_OPTION_SOUND)

    def _handleSettingsChange(self, eventKey):
        if self.themeTitleSelected:
            currentThemeIndex = list(THEME_DICT.keys()).index(CONFIGS["current_theme"])
            if eventKey == pygame.K_LEFT:
                CONFIGS["current_theme"] = list(THEME_DICT.keys())[
                    (currentThemeIndex - 1) % 5
                ]
            else:
                CONFIGS["current_theme"] = list(THEME_DICT.keys())[
                    (currentThemeIndex + 1) % 5
                ]
        else:
            currentSpeedIndex = SPEED_OPTIONS.index(
                CONFIGS["speed_diameters_per_second"]
            )
            if eventKey == pygame.K_LEFT:
                CONFIGS["speed_diameters_per_second"] = SPEED_OPTIONS[
                    (currentSpeedIndex - 1) % 3
                ]
            else:
                CONFIGS["speed_diameters_per_second"] = SPEED_OPTIONS[
                    (currentSpeedIndex + 1) % 3
                ]

    def _handleSave(self):
        updateColorTheme(CONFIGS["current_theme"])
        updateSpeed(CONFIGS["speed_diameters_per_second"])
        self.showInstructions = False
        self._displayTexts()
        time.sleep(2.5)
        self.showInstructions = True
        self._displayTexts()
