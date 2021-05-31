import pygame
from TextFormatter.TextFormatter import TextFormatter
from Colors.Colors import BACKGROUND_MENU_COLOR as BACKGROUND_COLOR
from Colors.Colors import green as GREEN


FONT = "Fonts/retro.ttf"


class MainMenu:

    def __init__(self, window):
        self.window = window
        self.window.screen.fill(BACKGROUND_COLOR)
        title = TextFormatter().formatText("PySnake", FONT, 90, GREEN)
        screenWidth, _ = self.window.getDimensions()
        self.window.screen.blit(
            title, (screenWidth/2 - (title.get_rect()[2]/2), 80))
        pygame.display.update()
