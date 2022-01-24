import numpy as np

def gen_wave(sound_length=1, freq=440, sampling_rate=44100, type="pulse_quarter"):
    quantity = int(sound_length * sampling_rate + 0.5)
    timing = np.linspace(0, sound_length, quantity + 1)  # 最後のタイミングも含めるので+1
    timing = np.delete(timing, -1)  # 0<=x<len とする
    func = eval("_" + type)
    return func(freq, timing)

def _zero(_, t):
    return t * 0

# 正弦波
def _sine(freq, t):
    return np.sin(2 * np.pi * freq * t)

# 矩形波（50%パルス波）
def _square(freq, t):
    # [0-pi] -> 1, [pi-2pi] -> -1
    return (np.ceil(t * freq * 2) % 2) * 2 - 1

# 25%パルス波
def _pulse_quarter(freq, t):
    return (np.ceil(t * freq * 4 - 1) % 4 == 0) * 2 - 1

# 12.5%パルス波
def _pulse_eighth(freq, t):
    return (np.ceil(t * freq * 8 - 1) % 8 == 0) * 2 - 1

# 三角波
def _triangle(freq, t):
    return np.abs((2 * t * freq - 1 / 2) % 2 - 1) * 2 - 1

# 階段三角波
def _triangle_stair(freq, t):
    s = np.abs((2 * t * freq - 1 / 2) % 2 - 1) * 16 + 0.5
    return s.astype("int64") / 8 - 1

# 階段三角波（ファミコン）
def _triangle_stair2(freq, t):
    s = list(range(16)) + list(range(15, -1, -1))
    t = (t * len(s) * freq) % len(s)
    return np.array([s[int(i)] / 7.5 - 1 for i in t])

# ノイズ(ファミコン風)
def _noise(freq, t):
    duration = t[-1]-t[0]
    coarse_x = np.linspace(t[0], t[-1], int(freq*20*duration)+1) # ここの倍率は要検討
    coarse_noise = np.random.uniform(-1, 1, size=coarse_x.shape[0])
    # 一次元のNearest Neighbor法
    tile_n = int(np.ceil(t.shape[0]/coarse_x.shape[0]))
    interpolate_noise = np.stack([coarse_noise for i in range(tile_n)], axis=-1)
    return interpolate_noise.flatten()[:t.shape[0]]