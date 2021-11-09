from img_collector import ImageCollector
from detect_stf import StfDetector
from detect_para import ParagraphDetector
from paragraph import Paragraph
import cv2


class Score:
    def __init__(self, path) -> None:
        self._path = path
        self._img = ImageCollector(path)

    def detect_lines(self):
        staff_qty = 0
        thresh_tmp = thresh = 128
        STEP = 16
        while thresh_tmp < 255:
            stf_detector = StfDetector(self._img.imgs[1])
            staff_tmp, flg, pitch = stf_detector.detect_stf()
            if flg == False:
                break
            thresh_tmp += STEP
            self._img.set_thresh(thresh_tmp)
            if len(staff_tmp) > staff_qty:
                staff_qty = len(staff_tmp)
                thresh = thresh_tmp
        else:
            if len(staff_tmp) == 0:
                print("五線譜を正しく読み取れません")
                return [], 0
        thresh += STEP
        self._img.set_thresh(thresh)
        stf_detector = StfDetector(self._img.imgs[1])
        staff, flg, pitch = stf_detector.detect_stf()

        para_detector = ParagraphDetector(self._img.imgs[1], self._img.info)
        paragraph = para_detector.detect_para(staff)

        return paragraph, pitch

    def register_stf(self, lines_data):
        self._paragraph = [Paragraph(item, idx)
                           for idx, item in enumerate(lines_data)]

    def labeling(self, pitch, i):
        self._img2 = self._img.imgs[1].copy()
        # map(lambda i: i.remove_staffs(self._img2), self._paragraph)
        [i.remove_staffs(self._img2) for i in self._paragraph]

        # テスト用出力
        cv2.imwrite('../result/lineout/test'+str(i)+'.png', self._img2)

        self._img3 = self._img2.copy()
        result = []
        for idx, item in enumerate(self._paragraph):
            top = 0 if idx == 0 else self._paragraph[idx - 1].bottom
            bottom = self._img.info[0] if idx == len(
                self._paragraph) - 1 else self._paragraph[idx + 1].top
            result.append(item.search_marble_f1(self._img3, top, bottom))
        return result

    @property
    def imgs(self):
        return self._img.imgs.copy()


class Note:
    def __init__(self) -> None:
        pass


class Rest(Note):
    def __init__(self) -> None:
        super().__init__()
