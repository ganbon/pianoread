import cv2
import numpy as np

class Staff:
    def __init__(self, data, no) -> None:
        self._no = no
        self._staff_lines = data
        self._margin_staff, self._margin_list = self.margin_ave(data)


    def margin_ave(self, data):
        margin = [data[i + 1][0] - data[i][0] for i in range(len(data) - 1)]
        margin_ave = sum(margin) / len(margin)
        return margin_ave, margin


    def remove_staff(self, img):
        _, w = img.shape[:2]
        POINT = w // 2
        OVERFLOW = 1
        MIN_LENGTH = w // 140
        middle_x1, middle_x2 = w * 2 // 5, w * 3 // 5
        crop_x1, crop_x2 = POINT - MIN_LENGTH * 4, POINT + MIN_LENGTH * 4
        for item in self._staff_lines:
            lists = []
            right_list = self.search_staff(item, img, POINT, w, MIN_LENGTH)
            left_list = self.search_staff(item, img, POINT, 0, MIN_LENGTH)
            middle_list = self.search_staff(item, img, middle_x1, middle_x2, MIN_LENGTH)

            lists = left_list + right_list
            lists = [i for i in lists if i[0] < crop_x1 or crop_x2 < i[0]]
            middle_list = [i for i in middle_list if crop_x1 <= i[0] <= crop_x2]
            lists.extend(middle_list)

            for item2 in lists:
                top = int(item2[1] - ((item[1] - 1) / 2 + OVERFLOW))
                bottom = int(item2[1] + ((item[1] - 1) / 2 + OVERFLOW))
                x = item2[0]
                img = cv2.line(img, (x, top), (x, bottom), 255, 1)


    def search_staff(self, data, img, x1, x2, min_length):
        OVERFLOW = 1
        ZONE_WIDTH_PART = int((data[1] - 1) / 2 + OVERFLOW)
        LIMIT_MARGIN = 3
        limits = [int(data[0] - ZONE_WIDTH_PART - LIMIT_MARGIN), int(data[0] + ZONE_WIDTH_PART + LIMIT_MARGIN)]
        lists = []
        tmp = []

        py = t_py = data[0]
        for x in range(x1, x2, 1 if x2 - x1 > 0 else -1):
            middle_judge, middle_count = self.judge_alone(img, x, py, ZONE_WIDTH_PART, limits)
            upper_judge, upper_count = self.judge_alone(img, x, py - 1, ZONE_WIDTH_PART, limits)
            lower_judge, lower_count = self.judge_alone(img, x, py + 1, ZONE_WIDTH_PART, limits)

            if not len(tmp):
                t_py = py

            if middle_judge:
                if upper_judge and lower_judge and upper_count > middle_count and lower_count > middle_count:
                    if upper_count > lower_count:
                        py -= 1
                    else:
                        py += 1
                elif upper_judge and upper_count > middle_count:
                    py -= 1
                elif lower_judge and lower_count > middle_count:
                    py += 1
                else:
                    pass
            else:
                if upper_judge and lower_judge:
                    if upper_count > lower_count:
                        py -= 1
                    else:
                        py += 1
                elif upper_judge:
                    py -= 1
                elif lower_judge:
                    py += 1
                else:
                    if len(tmp) > min_length:
                        lists.extend(tmp)
                    else:
                        py = t_py
                    tmp.clear()
                    continue

            tmp.append((x, py))

        if len(tmp) > min_length:
            lists.extend(tmp)

        return lists


    def judge_alone(self, img, x, py, width, limits):
        top_out = int(py - width - 1)
        bottom_out = int(py + width + 1)
        if top_out >= limits[0] and bottom_out <= limits[1] and img[top_out, x] == 255 and img[bottom_out, x] == 255:
            judge = True
        else:
            judge = False

        count = 0
        basic_point = width + 1
        for i in range(int(py - width), int(py + width + 1)):
            if img[i, x] == 0:
                count += (basic_point - abs(i - py)) * 2

        return judge, count


    def search_marble_f1(self, img):
        scan_y = [[i[0] - self._margin_staff / 2, i[0]] for i in self._staff_lines]
        scan_y = list(np.ravel(scan_y))
        scan_y += [self._staff_lines[-1][0] + self._margin_staff / 2]
        scan_y = [round(i) for i in scan_y]
        
        h, w = img.shape[:2]
        mask_margin = int(self._margin_staff) if int(self._margin_staff) % 2 else int(self._margin_staff) + 1
        mask = np.zeros((mask_margin, mask_margin), dtype=np.uint8)
        margin_r = mask_margin // 2
        cv2.circle(mask, center=(margin_r, margin_r), radius=margin_r, color=255, thickness=-1)

        lists = []
        for y in scan_y:
            lists.append(self.scan_marble_on_horizon(img, w, y, mask, margin_r))

        return [scan_y, lists, self._margin_staff]


    def scan_marble_on_horizon(self, img, w, y, mask, margin_r):
        list_ = []
        for i in range(margin_r, w - margin_r):
            if img[y, i] == 0:
                img_p = img[y - margin_r: y + margin_r + 1, i - margin_r: i + margin_r + 1]
                img_p = img_p & mask
                if np.count_nonzero(img_p == 255) <= img_p.size // 100:
                    list_.append(i)

        return list_
