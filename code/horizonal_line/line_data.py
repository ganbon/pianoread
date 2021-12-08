
from horizonal_line.mng_score import Score
#横線データの取得
def scoreline_data(path):
    PATH = path
    score = Score(path)
    lines_data, pitch = score.detect_lines()
    if pitch == 0:
        return
    score.register_stf(lines_data)
    return lines_data