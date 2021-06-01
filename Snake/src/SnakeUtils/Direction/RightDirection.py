from . import LeftDirection


class RightDirection:

    def move(self, body, diameter):
        snakePos = body[0]
        newBody = [[snakePos[0] + diameter, snakePos[1]]]
        for pos in body:
            newBody.append(pos)
        return newBody

    def canBeChangedTo(self, newDirection):
        return type(newDirection) not in (LeftDirection.LeftDirection, type(self))
