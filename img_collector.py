import math
import cv2
import numpy as np
from scipy import ndimage


class ImageCollector:
    def __init__(self, path):
        self._path = path
        self._img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)
        self.set_thresh(192)
        self._img = self.correct_tilt()
        self.set_thresh()
        self._h, self._w = self._img.shape[:2]


    def set_thresh(self, thresh=128):
        _, self._img_thresh = self.cvt_thresh(self._img, thresh)


    def cvt_thresh(self, img, thresh=128):
        return cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)


    def correct_tilt(self):
        reverse_img = cv2.bitwise_not(self._img_thresh)
        _, w = self._img_thresh.shape[:2]
        MIN_LINE_LENGTH = w // 3
        MAX_LINE_GAP = w // 5

        lines = cv2.HoughLinesP(reverse_img, 1, np.pi / 360, 100, MIN_LINE_LENGTH, MAX_LINE_GAP)

        HORIZONTAL = 0
        DIFF = 10       # 許容誤差 -> -10 - +10 を本来の水平線と考える
        sum_arg = 0
        count = 0
        for line in lines:
            for x1, y1, x2, y2 in line:
                arg = math.degrees(math.atan2((y2 - y1), (x2 - x1)))
                if arg > HORIZONTAL - DIFF and arg < HORIZONTAL + DIFF :
                    sum_arg += arg
                    count += 1

        ave_arg = (sum_arg / count) - HORIZONTAL if count else HORIZONTAL

        return ndimage.rotate(self._img, ave_arg, cval = 255)


    @property
    def imgs(self):
        return [self._img, self._img_thresh]


    @property
    def info(self):
        return [self._h, self._w]
