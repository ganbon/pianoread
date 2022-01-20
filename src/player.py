import numpy as np
import sys
import wave
import math
import csv
from itertools import groupby
from fractions import Fraction
import re

def synthesizer(file_name):
    sampling_rate = 44100  # サンプリングレートは一般的な44100Hz
    bpm = 156
    volume = {"master": 0.5,"square": 0.1, "pulse_quarter": 0.1, "pulse_eighth": 0.1, "triangle": 0.25, "sine": 0.5}
    func = {"square": square, "pulse_quarter": pulse_quarter, "pulse_eighth": pulse_eighth, "triangle": triangle, "sine": sine}
    define = ["square", "pulse_quarter", "pulse_quarter", "triangle", "pulse_eighth", "pulse_quarter"]

    # test_data = [[[("C4", 1)], 4], [[("C4", 1), ("E4", 1), ("G4", 1)], 4], [[("R", 0)], 2], [[("E4", 0.5), ("G4", 0.5), ("B4", 0.5)], 4]]

    whole_note = (60 / bpm) * 4  # 全音符の秒数

    data = import_data(file_name)
    y = []
    for item1, item2 in zip(data, define):
        y.append(gen_track(item1, sampling_rate, whole_note, func[item2]) * volume[item2])
    y = synthesize_wave(y) * volume["master"]

    # 演奏終了地点より後ろをカット
    for i, item in enumerate(y[::-1]):
        if item != 0:
            point = round(i - sampling_rate * 1)
            break
    y = y[:-point]

    # 量子化
    y = (y*32767).astype(np.int16)

    save_file = re.sub(r"^.*[/\\]|\.[^.]+", "", file_name)
    try:
        with wave.Wave_write("../dst/{}.wav".format(save_file)) as fp:
            fp.setframerate(sampling_rate)
            fp.setnchannels(1) # モノラル
            fp.setsampwidth(2) # 16ビット（バイト数を入力する）
            fp.writeframes(y.tobytes()) # バイナリ化
    except Exception as e:
        print(e)
        exit(1)

# CSVファイルの読み込み
def import_data(file_name):
    try:
        with open(file_name, "r", encoding="utf_8") as file:
            reader = csv.reader(file, skipinitialspace=True)
            data = [row for row in reader][1:]
    except FileNotFoundError as e:
        print("ファイルが見つかりません", e)
        exit(1)
    except Exception as e:
        print(e)
        exit(1)

    data.sort(key=lambda x: [int(x[0]), int(x[1])])
    data = [[list(row)[1:] for row in track] for key, track in groupby(data, key=lambda x: x[0])]
    data = [[[list(row)[1:] for row in track] for key, track in groupby(group, key=lambda x: x[0])] for group in data]
    
    for i, truck in enumerate(data):
        for j, unit in enumerate(truck):
            len = Fraction(1, Fraction(unit[0][1]))
            elm = [(note[0], float(note[2])) for note in unit]
            data[i][j] = [elm, len]

    return data

# トラックの生成
def gen_track(track_data, sampling_rate, whole_note, wave_generator):
    DEFAULT_LENGTH = 180
    y = np.zeros(sampling_rate * DEFAULT_LENGTH)
    t = 0

    for idx, elm in enumerate(track_data):
        length = elm[1]
        if idx + 1 < len(track_data) and in_next(elm[0], track_data[idx + 1][0]):
            elm[1] *= 0.92
        tmp = gen_unit(elm, sampling_rate, whole_note, wave_generator)
        x = math.ceil(sampling_rate * (t * whole_note))
        y[x:x + len(tmp)] += tmp
        t += length

    return y

# 次の音に現在の音と同じ音階が含まれているか判定
def in_next(current, next):
    for item_c in current:
        for item_n in next:
            if item_c[0] == item_n[0]:
                return True
    return False

# 単音/和音の生成
def gen_unit(notes, sampling_rate, whole_note, wave_generator):
    unit_length = whole_note * notes[1]  # ユニットの時間的な長さ

    # ユニット長をサンプリングレートで分割して間隔ごとの時間を求め、リストとする
    x = np.linspace(0, unit_length, round(sampling_rate * unit_length) + 1)
    x = np.delete(x, -1)  # 0<=x<len とする
    y = []

    for note in notes[0]:
        if note[0] == "R":
            y.append(np.zeros(len(x)))
        else:
            # 波のvelocityを調整し、リストに追加
            y.append(wave_generator(note_to_freq(note[0]), x) * note[1])

    return synthesize_wave(y)

# 音波の合成
def synthesize_wave(waves):
    res = np.zeros(len(waves[0]))  # 合成先のダミーリスト

    for wave in waves:
        res += wave
    return res

# 音階→周波数
def note_to_freq(notestr):
    key, octave = notestr[:-1], notestr[-1]
    keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    # 周波数起点はA（ラ）からなのに、オクターブはC（ド）からなので周期を調整する
    return 27.5 * 2 ** (int(octave) + (keys.index(key) - 9) / 12)

# 正弦波
def sine(freq, t):
    return np.sin(2 * np.pi * freq * t)

# 矩形波（50%パルス波）
def square(freq, t):
    # [0-pi] -> 1, [pi-2pi] -> -1
    return (np.ceil(t * freq * 2) % 2) * 2 - 1

# 25%パルス波
def pulse_quarter(freq, t):
    return (np.ceil(t * freq * 4 - 1) % 4 == 0) * 2 - 1

# 12.5%パルス波
def pulse_eighth(freq, t):
    return (np.ceil(t * freq * 8 - 1) % 8 == 0) * 2 - 1

# 三角波
def triangle(freq, t):
    return np.abs((2 * t * freq - 1 / 2) % 2 - 1) * 2 - 1

# ノイズ(ファミコン風)
def noise(freq, t):
    duration = t[-1]-t[0]
    coarse_x = np.linspace(t[0], t[-1], int(freq*20*duration)+1) # ここの倍率は要検討
    coarse_noise = np.random.uniform(-1, 1, size=coarse_x.shape[0])
    # 一次元のNearest Neighbor法
    tile_n = int(np.ceil(t.shape[0]/coarse_x.shape[0]))
    interpolate_noise = np.stack([coarse_noise for i in range(tile_n)], axis=-1)
    return interpolate_noise.flatten()[:t.shape[0]]


if __name__ == '__main__':
    args = sys.argv
    if 2 <= len(args):
        synthesizer(args[1])
    else:
        print("引数が不足（入力ファイルを指定してください）")

# トラックの書式
# [ [ユニット], [ [(単音), (音階, ベロシティ)], 長さ ] ]
# [[[("C4", 1)], 4], [[("C4", 1), ("E4", 1), ("G4", 1)], 4], [[("R", 0)], 2], [[("E4", 0.5), ("G4", 0.5), ("B4", 0.5)], 4]]