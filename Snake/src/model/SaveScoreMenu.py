import pygame
import time
from random import randint
from model.TextFormatter.TextFormatter import TextFormatter
from model.Config.configParser import CONFIGS
from model.data.ScoresManager import ScoresManager
import model.MainMenu

THEME = CONFIGS["current_theme"]
BACKGROUND_COLOR = CONFIGS["colors"][THEME]["background"]
LOGO_COLOR = CONFIGS["colors"][THEME]["logo"]
FONT = CONFIGS["font"]

SELECT_OPTION_SOUND_PATH = CONFIGS["sounds"]["select_option"]
KEYBOARD_PRESS_SOUND_PATH = CONFIGS["sounds"]["keyboard_press_sound"]
pygame.mixer.init()
SELECT_OPTION_SOUND = pygame.mixer.Sound(
    SELECT_OPTION_SOUND_PATH)
KEYBOARD_PRESS_SOUND = pygame.mixer.Sound(KEYBOARD_PRESS_SOUND_PATH)
SELECT_OPTION_SOUND.set_volume(0.5)
KEYBOARD_PRESS_SOUND.set_volume(0.5)


class SaveScoreMenu:

    def __init__(self, window, score, level):
        self.window = window
        self.open = True
        self.score = score
        self.level = level
        self.id = f'randomid{randint(10000,99999)}'
        self._displayTexts()
        self._loop()

    def _displayTexts(self):
        '''
        Displays the text in the main menu.
        '''
        self.window.screen.fill(BACKGROUND_COLOR)
        title = TextFormatter().formatText(
            f"YOU SCORED {self.score} POINTS AT LEVEL {self.level}", FONT, 75, LOGO_COLOR)
        info = TextFormatter().formatText(
            "START TYPING YOUR ID TO REGISTER YOUR SCORE...", FONT, 60, LOGO_COLOR)
        idView = TextFormatter().formatText(
            f"{str(self.id)}{'I' if time.gmtime().tm_sec % 2 == 0 else ''}", FONT, 120, LOGO_COLOR)
        saveInfo = TextFormatter().formatText(
            "PRESS ENTER TO SAVE YOUR SCORE.", FONT, 90, LOGO_COLOR)
        screenWidth, _ = self.window.getDimensions()
        self.window.screen.blit(
            title, (screenWidth/2 - (title.get_rect()[2]/2), 20))
        self.window.screen.blit(
            info, (screenWidth/2 - (info.get_rect()[2]/2), 150))
        self.window.screen.blit(
            idView, (screenWidth/2 - (idView.get_rect()[2]/2), 300))
        self.window.screen.blit(
            saveInfo, (screenWidth/2 - (saveInfo.get_rect()[2]/2), 600))
        pygame.display.update()

    def _emptyId(self):
        for c in self.id:
            if c != ' ':
                return False
        return True

    def _loop(self):
        '''
        Executes the main loop of the main menu,
        which is in charge of identifying which option is selected
        and updating the information graphically in the correct moment.
        '''
        while self.open:
            time.sleep(0.1)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self._emptyId():
                            self.id = f'randomid{randint(10000,99999)}'
                        self.open = False
                        pygame.mixer.Sound.play(SELECT_OPTION_SOUND)
                        ScoresManager().save(self.id, self.score, self.level)
                        model.MainMenu.MainMenu(self.window)
                    elif event.key == pygame.K_BACKSPACE:
                        pygame.mixer.Sound.play(KEYBOARD_PRESS_SOUND)
                        self.id = self.id[0:-1]
                    else:
                        pygame.mixer.Sound.play(KEYBOARD_PRESS_SOUND)
                        self.id += event.unicode
                if event.type == pygame.QUIT:
                    pygame.mixer.Sound.play(SELECT_OPTION_SOUND)
                    time.sleep(0.2)
                    self.open = False
                    self.window.stopRunning()
            self._displayTexts()
