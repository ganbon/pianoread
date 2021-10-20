from scipy.ndimage import interpolation
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
                exit(1)
        thresh += STEP
        self._img.set_thresh(thresh)
        stf_detector = StfDetector(self._img.imgs[1])
        staff, flg, pitch = stf_detector.detect_stf()

        para_detector = ParagraphDetector(self._img.imgs[1], self._img.info)
        paragraph = para_detector.detect_para(staff)

        return paragraph, pitch


    def register_stf(self, lines_data):
        self._paragraph = [Paragraph(item, idx) for idx, item in enumerate(lines_data)]


    def labeling(self, pitch):
        self._img2 = self._img.imgs[1].copy()
        # map(lambda i: i.remove_staffs(self._img2), self._paragraph)
        [i.remove_staffs(self._img2) for i in self._paragraph]

        # テスト用出力
        cv2.imwrite('data/dst/test.png', self._img2)

        self._img3 = self._img2.copy()
        # self._img3 = cv2.resize(self._img3, dsize=None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
        # self._img.remove_line(self._img3, thresh=pitch, min_l=pitch * 3, max_gap=1, diff=85)
        # self._img3 = cv2.resize(self._img3, dsize=None, fx=0.25, fy=0.25, interpolation=cv2.INTER_NEAREST)
        result = [i.search_marble_f1(self._img3) for i in self._paragraph]
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