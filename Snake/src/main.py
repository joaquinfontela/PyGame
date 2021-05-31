from Window import Window
import os

if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    w = Window(1200, 720)
    w.display()
