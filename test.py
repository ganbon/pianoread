import time
import numpy as np
from scipy.io import wavfile
# パラメータ
FREQ = 261.626          # 生成するサイン波の周波数（note#60 C4 ド）
SAMPLE_RATE = 44100     # サンプリングレート
# 16bitのwavファイルを作成
wavfile.write("do.wav", SAMPLE_RATE,
              (np.sin(np.arange(SAMPLE_RATE) * FREQ * np.pi * 2 / SAMPLE_RATE) * 32767.0).astype(np.int16))