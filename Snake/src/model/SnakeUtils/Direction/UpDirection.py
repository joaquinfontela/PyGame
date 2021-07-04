from . import DownDirection


class UpDirection:

    def move(self, body, diameter):
        snakePos = body[0]
        newBody = [[snakePos[0], snakePos[1] - diameter]]
        for pos in body:
            newBody.append(pos)
        return newBody

    def canBeChangedTo(self, newDirection):
        return type(newDirection) not in (DownDirection.DownDirection, type(self))
