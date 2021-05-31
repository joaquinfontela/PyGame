import pygame


class TextFormatter:

    def __init__(self):
        pass

    def formatText(self, msg, font, size, color):
        font = pygame.font.Font(font, size)
        text = font.render(msg, 0, color)
        return text
