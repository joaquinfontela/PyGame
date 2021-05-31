import pygame
from MainMenu import MainMenu
from EventHandler import EventHandler


class Window:

    def __init__(self, width, height):
        '''
        Initializes a Window object with width and height attributes.
        '''
        pygame.init()
        print(sorted(pygame.font.get_fonts()))
        self.width = width
        self.height = height
        self._screen = pygame.display.set_mode((width, height))
        self.running = False

    @property
    def screen(self):
        return self._screen

    def getDimensions(self):
        return (self.width, self.height)

    def display(self):
        self._setBackgroundColor(0, 0, 0)
        pygame.display.flip()
        pygame.display.set_caption('PySnake')
        self.running = True
        self._mainLoop()

    def _mainLoop(self):
        while self.running:
            for event in pygame.event.get():
                EventHandler(self).handleEvent(event)

            MainMenu(self)

    def stopRunning(self):
        self.running = False

    def _setBackgroundColor(self, r, g, b):
        color = (r, g, b)
        self._screen.fill(color)
