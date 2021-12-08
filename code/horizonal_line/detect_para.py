from horizonal_line.detect_bar import BarDetector
import cv2

class ParagraphDetector:
    def __init__(self, img, info) -> None:
        self._img = img
        self._w = info[1]

    
    def detect_para(self, staff):
        para_data = []
        i = 0
        while i < len(staff) - 1:
            top_y = int(staff[i][0][0] - (staff[i][0][1] - 1) / 2)
            bottom_y = int(staff[i + 1][-1][0] + (staff[i + 1][-1][1] - 1) / 2)
            img_part = self._img[top_y: bottom_y, 0: self._w]
            bar_detector = BarDetector(img_part)
            bar_data = bar_detector.detect_bar()

            if len(bar_data) >= 2:
                para_data.append([staff[i], staff[i + 1]])
                i += 1
            else:
                para_data.append([staff[i]])
            i += 1
        if i == len(staff) - 1:
            para_data.append([staff[i]])

        return para_data
