import pygame


class Window:
    def __init__(self, width, height):
        """
        Initializes a Window object with width and height attributes.
        """
        pygame.init()
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
        icon = pygame.image.load("model/images/icon.png")
        pygame.display.set_icon(icon)
        pygame.mouse.set_visible(False)
        pygame.display.flip()
        pygame.display.set_caption("MemoPinball")
        self.running = True
        self._mainLoop()

    def _mainLoop(self):
        """
        Initializes the main loop of the application.
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stopRunning()

            # MainMenu(self)
            continue

    def stopRunning(self):
        self.running = False
        quit()
