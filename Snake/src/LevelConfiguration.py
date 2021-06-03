from pygame.constants import SYSTEM_CURSOR_SIZENWSE
from Config.configParser import CONFIGS
from SnakeUtils.Direction.Direction import Direction
from SnakeUtils.Direction.RightDirection import RightDirection
from SnakeUtils.Direction.DownDirection import DownDirection

CIRCLE_DIAMETER = CONFIGS["circle_diameter"]
CIRCLE_RADIUS = int(CIRCLE_DIAMETER/2)


class LevelConfiguration:

    def __init__(self, window, level):
        self.window = window
        self.level = level

    def getLevelWalls(self):
        if self.level == 1:
            return []
        elif self.level == 2:
            return self._getLevel2Walls()
        elif self.level == 3:
            return self._getLevel3Walls()
        elif self.level == 4:
            return self._getLevel4Walls()
        elif self.level == 5:
            return self._getLevel5Walls()
        elif self.level == 6:
            return self._getLevel6Walls()
        elif self.level == 7:
            return self._getLevel7Walls()
        elif self.level == 8:
            return self._getLevel8Walls()
        elif self.level == 9:
            return self._getLevel9Walls()
        elif self.level == 10:
            return self._getLevel10Walls()
        else:
            raise Exception()

    def getInitialPosAndDirection(self):
        screenWidth, screenHeight = self.window.getDimensions()
        if self.level in (1, 2):
            pos = [int(CIRCLE_RADIUS * 21), int(CIRCLE_RADIUS * 21)]
            return [[pos[0], pos[1]], [pos[0] - CIRCLE_DIAMETER, pos[1]],
                    [pos[0] - 2 * CIRCLE_DIAMETER, pos[1]
                     ], [pos[0] - 3 * CIRCLE_DIAMETER, pos[1]],
                    [pos[0] - 4 * CIRCLE_DIAMETER, pos[1]]], Direction(self.window, RightDirection())
        if self.level in (3, 4, 5, 7):
            pos = [int(screenWidth/4) + CIRCLE_DIAMETER,
                   int(screenHeight/2) + CIRCLE_DIAMETER/2]
            return [[pos[0], pos[1]], [pos[0], pos[1] - CIRCLE_DIAMETER],
                    [pos[0], pos[1] - 2 * CIRCLE_DIAMETER
                     ], [pos[0], pos[1] - 3 * CIRCLE_DIAMETER],
                    [pos[0], pos[1] - 4 * CIRCLE_DIAMETER]], Direction(self.window, DownDirection())
        if self.level == 9:
            pos = [CIRCLE_RADIUS + 5 * CIRCLE_DIAMETER,
                   screenHeight - 3 * CIRCLE_RADIUS]
            return [[pos[0], pos[1]], [pos[0] - CIRCLE_DIAMETER, pos[1]],
                    [pos[0] - 2 * CIRCLE_DIAMETER, pos[1]
                     ], [pos[0] - 3 * CIRCLE_DIAMETER, pos[1]],
                    [pos[0] - 4 * CIRCLE_DIAMETER, pos[1]]], Direction(self.window, RightDirection())
        if self.level in (6, 8, 10):
            pos = [CIRCLE_RADIUS + 5 * CIRCLE_DIAMETER,
                   screenHeight - CIRCLE_RADIUS]
            return [[pos[0], pos[1]], [pos[0] - CIRCLE_DIAMETER, pos[1]],
                    [pos[0] - 2 * CIRCLE_DIAMETER, pos[1]
                     ], [pos[0] - 3 * CIRCLE_DIAMETER, pos[1]],
                    [pos[0] - 4 * CIRCLE_DIAMETER, pos[1]]], Direction(self.window, RightDirection())

    def _getLevel2Walls(self):
        walls = []
        screenWidth, screenHeight = self.window.getDimensions()
        for x in range(CIRCLE_RADIUS, screenWidth, CIRCLE_DIAMETER):
            walls.append([x, CIRCLE_RADIUS])
            walls.append([x, screenHeight - CIRCLE_RADIUS])
        for y in range(CIRCLE_RADIUS * 3, screenHeight - CIRCLE_RADIUS * 3 + 1, CIRCLE_DIAMETER):
            walls.append([CIRCLE_RADIUS, y])
            walls.append([screenWidth - CIRCLE_RADIUS, y])
        return walls

    def _getLevel3Walls(self):
        walls = []
        screenWidth, screenHeight = self.window.getDimensions()
        for x in range(CIRCLE_RADIUS, int(screenWidth/4) + 1, CIRCLE_DIAMETER):
            walls.append([x, CIRCLE_RADIUS])
            walls.append([x, screenHeight - CIRCLE_RADIUS])
            walls.append([screenWidth - x, CIRCLE_RADIUS])
            walls.append([screenWidth - x, screenHeight - CIRCLE_RADIUS])
        for y in range(CIRCLE_RADIUS * 3, int(screenHeight/4) + 1, CIRCLE_DIAMETER):
            walls.append([CIRCLE_RADIUS, y])
            walls.append([CIRCLE_RADIUS, screenHeight - y])
            walls.append([screenWidth - CIRCLE_RADIUS, y])
            walls.append([screenWidth - CIRCLE_RADIUS, screenHeight - y])
        for x in range(int(screenWidth/4) + 2 * CIRCLE_DIAMETER,
                       3 * int(screenWidth/4) - 2 * CIRCLE_DIAMETER, CIRCLE_DIAMETER):
            for y in range(int(screenHeight/4) + 2 * CIRCLE_DIAMETER,
                           3 * int(screenHeight/4) - 2 * CIRCLE_DIAMETER, CIRCLE_DIAMETER):
                walls.append([x, y])
        return walls

    def _getLevel4Walls(self):
        walls = []
        screenWidth, screenHeight = self.window.getDimensions()
        for y in range(CIRCLE_RADIUS, screenHeight - CIRCLE_RADIUS + 1, CIRCLE_DIAMETER):
            walls.append([int(screenWidth/2) - CIRCLE_RADIUS, y])
            walls.append([int(screenWidth/2) + CIRCLE_RADIUS, y])
        return walls

    def _getLevel5Walls(self):
        walls = []
        screenWidth, screenHeight = self.window.getDimensions()
        for x in range(4 * CIRCLE_DIAMETER + CIRCLE_RADIUS,
                       screenWidth - 4 * CIRCLE_DIAMETER - CIRCLE_RADIUS - 1, CIRCLE_DIAMETER * 5):
            for y in range(int(screenHeight/6) + CIRCLE_RADIUS, 5 * int(screenHeight/6) + CIRCLE_RADIUS, CIRCLE_DIAMETER):
                walls.append([x, y])
        return walls

    def _getLevel6Walls(self):
        walls = []
        screenWidth, screenHeight = self.window.getDimensions()
        for x in range(CIRCLE_RADIUS, screenWidth - CIRCLE_RADIUS + 1, CIRCLE_DIAMETER):
            walls.append([x, int(screenHeight/2) + CIRCLE_RADIUS])
            walls.append([x, int(screenHeight/2) - CIRCLE_RADIUS])
        walls += self._getLevel4Walls()
        return walls

    def _getLevel7Walls(self):
        screenWidth, screenHeight = self.window.getDimensions()
        walls = self._getLevel2Walls()
        for x in range(3 * CIRCLE_RADIUS, int(screenWidth/4) + CIRCLE_RADIUS + 1, CIRCLE_DIAMETER):
            walls.append([x, screenHeight/2 - CIRCLE_RADIUS])
            walls.append([x, screenHeight/2 + CIRCLE_RADIUS])
            walls.append([screenWidth - x, screenHeight/2 - CIRCLE_RADIUS])
            walls.append([screenWidth - x, screenHeight/2 + CIRCLE_RADIUS])
        for y in range(3 * CIRCLE_RADIUS, int(screenHeight/4) + CIRCLE_RADIUS + 1, CIRCLE_DIAMETER):
            walls.append([screenWidth/2 - CIRCLE_RADIUS, y])
            walls.append([screenWidth/2 + CIRCLE_RADIUS, y])
            walls.append([screenWidth/2 - CIRCLE_RADIUS, screenHeight - y])
            walls.append([screenWidth/2 + CIRCLE_RADIUS, screenHeight - y])
        return walls

    def _getLevel8Walls(self):
        walls = []
        screenWidth, screenHeight = self.window.getDimensions()
        for x in range(CIRCLE_RADIUS, screenHeight - CIRCLE_RADIUS + 1, CIRCLE_DIAMETER):
            walls.append([x, x])
            walls.append([screenWidth - x, x])
        return walls

    def _getLevel9Walls(self):
        walls = self._getLevel2Walls()
        walls += self._getLevel5Walls()
        screenWidth, screenHeight = self.window.getDimensions()
        for x in range(4 * CIRCLE_DIAMETER + CIRCLE_RADIUS,
                       screenWidth - 4 * CIRCLE_DIAMETER - CIRCLE_RADIUS - 1, CIRCLE_DIAMETER):
            walls.append([x, int(screenHeight/2) - CIRCLE_RADIUS])
            walls.append([x, int(screenHeight/2) + CIRCLE_RADIUS])
        return walls

    def _getLevel10Walls(self):
        walls = []
        screenWidth, screenHeight = self.window.getDimensions()
        for x in range(3 * CIRCLE_RADIUS, screenWidth - 5 * CIRCLE_RADIUS + 1, CIRCLE_DIAMETER * 8):
            for y in range(3 * CIRCLE_RADIUS, screenHeight - 5 * CIRCLE_RADIUS + 1, CIRCLE_DIAMETER * 4):
                walls.append([x, y])
                walls.append([x + 2 * CIRCLE_DIAMETER, y])
                walls.append([x, y + 2 * CIRCLE_DIAMETER])
                walls.append([x + 2 * CIRCLE_DIAMETER,
                             y + 2 * CIRCLE_DIAMETER])
        for x in range(11 * CIRCLE_RADIUS, screenWidth - 3 * CIRCLE_RADIUS + 1, CIRCLE_DIAMETER * 8):
            for y in range(5 * CIRCLE_RADIUS, screenHeight - 3 * CIRCLE_RADIUS + 1, CIRCLE_DIAMETER * 4):
                walls.append([x, y])
                walls.append([x + 2 * CIRCLE_DIAMETER, y])
                if y + 2 * CIRCLE_DIAMETER < screenHeight - CIRCLE_RADIUS:
                    walls.append([x, y + 2 * CIRCLE_DIAMETER])
                    walls.append([x + 2 * CIRCLE_DIAMETER,
                                  y + 2 * CIRCLE_DIAMETER])
        return walls
