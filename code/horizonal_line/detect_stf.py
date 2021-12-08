from horizonal_line.detect_line import LineDetector
import numpy as np


class StfDetector(LineDetector):
    def __init__(self, img) -> None:
        super().__init__(img)

    
    def detect_stf(self):
        THRESHOLD = 2
        data = super().extract_lines(self._img, thresh=THRESHOLD)
        shaped_data = super().data_shaping(data)
        grouped_data, line_pitch = self.grouping_data(shaped_data)
        staff_data = self.complement_noise(grouped_data)

        require_reprocess = False
        for item in grouped_data:
            if 5 > len(item) > 1 or len(staff_data) == 0:
                require_reprocess = True
                break

        return staff_data, require_reprocess, line_pitch


    def grouping_data(self, data):
        dist_basis = self.meas_distance(data)
        result = []
        tmp = [data[0]] if len(data) else []

        LINE_PITCH_DIFF = 2
        for i in range(1, len(data)):
            if abs(data[i][0] - data[i - 1][0] - dist_basis) <= LINE_PITCH_DIFF:
                tmp.append(data[i])
            else:
                result.append(tmp)
                tmp = [data[i]]
        result.append(tmp)

        return result, dist_basis


    def meas_distance(self, data):
        distance = {}
        for i in range(len(data) - 1):
            key = data[i + 1][0] - data[i][0]
            distance[key] = distance[key] + 1 if key in distance else 1

        result = np.array([kv[0] for kv in distance.items() if kv[1] == max(distance.values())])

        return np.mean(result) if len(result) else 0

    
    def complement_noise(self, grouped_data):
        return [i for i in grouped_data if len(i) == 5]
