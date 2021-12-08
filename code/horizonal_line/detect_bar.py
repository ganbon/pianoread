from horizonal_line.detect_line import LineDetector

class BarDetector(LineDetector):
    def __init__(self, img) -> None:
        super().__init__(img)


    def detect_bar(self):
        THRESHOLD, DIRECTION = 1.05, 1
        data = super().extract_lines(self._img, dire=DIRECTION, thresh=THRESHOLD)
        shaped_data = super().data_shaping(data)

        return shaped_data