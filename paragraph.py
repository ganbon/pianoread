from staff import Staff

class Paragraph:
    def __init__(self, data, no) -> None:
        self.staff_qty = len(data)
        self._no = no
        self._staff = [Staff(item, idx) for idx, item in enumerate(data)]
        self._top = self._staff[0].top
        self._bottom = self._staff[-1].bottom


    def remove_staffs(self, img):
        [i.remove_staff(img) for i in self._staff]


    def search_marble_f1(self, img, top_p, bottom_p):
        result = []
        for idx, item in enumerate(self._staff):
            top = top_p if idx == 0 else self._staff[idx - 1].bottom
            bottom = bottom_p if idx == len(self._staff) - 1 else self._staff[idx + 1].top
            result.append(item.search_marble_f1(img, top, bottom))

        return result


    @property
    def top(self):
        return self._top


    @property
    def bottom(self):
        return self._bottom
