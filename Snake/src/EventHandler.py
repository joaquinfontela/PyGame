import pygame
from Handler.CloseWindow import CloseWindow


class EventHandler:

    def __init__(self, window):
        self.window = window

    def handleEvent(self, e):
        if e.type == pygame.QUIT:
            CloseWindow(self.window)
