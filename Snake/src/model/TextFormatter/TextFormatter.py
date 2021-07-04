import pygame


class TextFormatter:

    def __init__(self):
        pass

    def formatText(self, msg, font, size, color, alpha=255):
        font = pygame.font.Font(font, size)
        text = font.render(msg, 0, color)
        text.set_alpha(alpha)
        return text
