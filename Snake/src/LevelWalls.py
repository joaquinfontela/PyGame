from Config.configParser import CONFIGS

CIRCLE_DIAMETER = CONFIGS["circle_diameter"]
CIRCLE_RADIUS = int(CIRCLE_DIAMETER/2)


class LevelWalls:

    def getLevelWalls(self, window, level):
        self.window = window
        if level == 1:
            return []
        elif level == 2:
            return self._getLevel2Walls()

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
