import cv2 as cv
import numpy as np
import math

BLACK = (0, 0, 0)
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
YELLOW = (0, 255, 255)
CYAN = (255, 255, 0)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)

class Window:
    """Create a window with an image."""
    def __init__(self, win, img):
        self.win = win
        self.img0 = img.copy()
        self.img = img
        self.d = 2
        self.col = GREEN
        cv.imshow(win, img)
        cv.setMouseCallback(win, self.mouse)
        self.text = 'Overlay of window: ' + self.win
        cv.displayOverlay(self.win, self.text, 2000)
        cv.displayStatusBar(self.win, 'Statusbar', 2000)

        cv.createButton('Button' + win, print)
        cv.createTrackbar('x', win, 100, 255, self.trackbar)

    def mouse(self, event, x, y, *args):
        """Mouse callback."""
        global k
        # print('mouse in', self.win, event, x, y, *args)
        h, w = self.img.shape[:2]
        self.img = self.img0.copy()

        # draw a crosshair
        cv.line(self.img, (0, y), (w, y), RED, 1)
        cv.line(self.img, (x, 0), (x, h), RED, 1)

        # draw a shape (rectangle, circle)
        if event == 1:
            self.p0 = x, y
            self.text = 'p0 = ({}, {})'.format(x, y)
            cv.displayStatusBar(self.win, self.text, 2000)
            cv.displayOverlay(self.win, self.text, 1000)
            
        elif event == 0:
            k = App.k
            if k == 'r':
                cv.rectangle(self.img, self.p0, (x, y), self.col, self.d)
            elif k == 'l':
                cv.line(self.img, self.p0, (x, y), self.col, self.d)
            elif k == 'c':
                dx = x - self.p0[0]
                dy = y - self.p0[1]
                r = int(math.sqrt(dx**2 + dy**2))
                cv.circle(self.img, self.p0, r, self.col, self.d)
        
        cv.imshow(self.win, self.img)

    def trackbar(self, x):
        """Trackbar callback function"""
        self.x = x
        text = 'Trackbar = {}'.format(x)
        cv.displayOverlay(self.win, text, 1000)
        cv.imshow(self.win, self.img)

class App:
    k = ''
    def __init__(self):
        img = np.zeros((200, 600, 3), np.uint8)
        img[:] = 127

        Window('image', img)
        Window('image2', img)

    def run(self):
        """Run the main event loop."""
        while App.k != 'q':
            App.k = chr(cv.waitKey(0))
            
        cv.destroyAllWindows()

if __name__ == '__main__':
    App().run()