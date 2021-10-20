from staff import Staff

class Paragraph:
    def __init__(self, data, no) -> None:
        self.staff_qty = len(data)
        self._no = no
        self._staff = [Staff(item, idx) for idx, item in enumerate(data)]


    def remove_staffs(self, img):
        [i.remove_staff(img) for i in self._staff]


    def search_marble_f1(self, img):
        result = [i.search_marble_f1(img) for i in self._staff]
        return result
