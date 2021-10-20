import cv2

class Prot:
    def __init__(self) -> None:
        pass


    def export_img(self, imgs):
        for i, img in enumerate(imgs):
            cv2.imwrite('data/dst/img_{:02}.png'.format(i), img)


    def paragraph(self, data, img_thresh):
        img = img_thresh.copy()
        _, w = img.shape[:2]
        self._img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        for idx, item1 in enumerate(data):
            for item2 in item1:
                for item3 in item2:
                    color_list = [(255, 0, 0), (0, 0, 255)]
                    color = color_list[idx % 2]
                    lists = [(item3[0] - (item3[1] - 1) / 2) + i for i in range(item3[1])]
                    for y in lists:
                        y = int(y)
                        self._img_rgb = cv2.line(self._img_rgb, (0, y), (w, y), color, 1)

        cv2.imwrite('data/dst/paragraph.png', self._img_rgb)


    def marbles(self, marbles):
        for i1 in marbles:
            for i2 in i1:
                margin = int(i2[2])
                for j1, j2 in zip(i2[0], i2[1]):
                    for j3 in j2:
                        cv2.circle(self._img_rgb, center=(j3, j1), radius=margin // 2, color=(0, 255, 0), thickness=-1)

        cv2.imwrite('data/dst/marble.png', self._img_rgb)
