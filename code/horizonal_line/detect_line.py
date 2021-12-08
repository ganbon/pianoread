import cv2
import numpy as np

class LineDetector:
    def __init__(self, img) -> None:
        self._img = img.copy()


    def extract_lines(self, img, dire=0, thresh=2):
        if dire == 1:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        h, w = img.shape[:2]
        
        line_list = []
        for r in range(h):
            line_list.append(self.count_conse_dot(img, r, w))

        data = [index for index, item in enumerate(line_list) if item >= w // thresh]

        return data


    def count_conse_dot(self, img, r, w):
        max = count = gap = 0
        MAX_GAP = 6

        for i in range(w):
            if img.item(r, i) == 0:
                count += 1 + gap
                gap = 0
                if count > max:
                    max = count
            else:
                gap += 1

            if gap > MAX_GAP:
                count = gap = 0

        return max


    def data_shaping(self, data):
        shaped_data = []
        tmp = []
        for i, item in enumerate(data):
            tmp.append(item)
            if i == len(data) - 1 or item + 1 != data[i + 1]:
                y = np.mean(tmp)
                weight = len(tmp)
                shaped_data.append((y, weight))
                tmp.clear()

        return shaped_data
