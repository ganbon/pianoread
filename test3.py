import numpy as np
import wave

def synthesis():
    sampling_rate = 44100 # サンプリングレートは44100Hz
    x = np.linspace(0, 1, sampling_rate*1+1)
    y = square(note_to_freq('C4'), x)
    y = np.concatenate([y, square(note_to_freq('D4'), x)])
    y = np.concatenate([y, square(note_to_freq('E4'), x)])
    y = np.concatenate([y, square(note_to_freq('F4'), x)])
    y = np.concatenate([y, square(note_to_freq('G4'), x)])

    # 量子化
    y = (y*32767).astype(np.int16)

    with wave.Wave_write("a_square.wav") as fp:
        fp.setframerate(sampling_rate)
        fp.setnchannels(1) # モノラル
        fp.setsampwidth(2) # 16ビット（バイト数を入力する）
        fp.writeframes(y.tobytes()) # バイナリ化

# 音階→周波数
def note_to_freq(notestr):
    key, octave = notestr[:-1], notestr[-1]
    keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    # 周波数起点はA（ラ）からなのに、オクターブはC（ド）からなので周期を調整する
    return 27.5 * 2 ** (int(octave) + (keys.index(key)-9)/12)

# 矩形波
def square(freq, t):
    # [0-pi] -> 1, [pi-2pi] -> -1
    return (np.ceil(t * freq * 2) % 2) * 2 - 1

if __name__ == '__main__':
    synthesis()