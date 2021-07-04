class Direction:

    def __init__(self, window, state):
        self.window = window
        self.lastPoppedBodyPosition = None
        self.state = state

    def getLastPoppedBodyPosition(self):
        return self.lastPoppedBodyPosition

    def move(self, body, diameter):
        newBody = self.state.move(body, diameter)
        self.lastPoppedBodyPosition = newBody.pop()
        return newBody

    def _canBeChangedTo(self, newState):
        return self.state.canBeChangedTo(newState)

    def changeState(self, newState):
        if self._canBeChangedTo(newState):
            self.state = newState
