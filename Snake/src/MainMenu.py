import pygame
from pygame.constants import KEYUP
from TextFormatter.TextFormatter import TextFormatter
from Colors.Colors import BACKGROUND_MENU_COLOR as BACKGROUND_COLOR
from Colors.Colors import green as GREEN, white as WHITE
from Game import Game


FONT = "Fonts/retro.ttf"


class MainMenu:

    def __init__(self, window):
        self.window = window
        self.open = True
        self.playSelected = True
        self._displayTexts()
        self._loop()

    def _displayTexts(self):
        self.window.screen.fill(BACKGROUND_COLOR)
        title = TextFormatter().formatText("PySnake", FONT, 150, GREEN)
        playButton = TextFormatter().formatText(
            "PLAY", FONT, 100, GREEN if self.playSelected else WHITE)
        quitButton = TextFormatter().formatText(
            "QUIT", FONT, 100, WHITE if self.playSelected else GREEN)
        screenWidth, _ = self.window.getDimensions()
        self.window.screen.blit(
            title, (screenWidth/2 - (title.get_rect()[2]/2), 80))
        self.window.screen.blit(
            playButton, (screenWidth/2 - (playButton.get_rect()[2]/2), 400))
        self.window.screen.blit(
            quitButton, (screenWidth/2 - (quitButton.get_rect()[2]/2), 525))
        pygame.display.update()

    def _loop(self):
        while self.open:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_DOWN, pygame.K_UP):
                        self._switchPlaySelected()
                        self._displayTexts()
                    if event.key == pygame.K_RETURN:
                        Game(self.window)
                if event.type == pygame.QUIT or \
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not self.playSelected):
                    self.open = False
                    self.window.stopRunning()

    def _switchPlaySelected(self):
        self.playSelected = not self.playSelected
