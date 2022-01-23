import numpy as np
import matplotlib.pyplot as plt

# 階段三角波
def _triangle_stair(freq, t):
    s = np.abs((2 * t * freq - 1 / 2) % 2 - 1) * 16 + 0.5
    return s.astype("int64") / 8 - 1

x = np.linspace(0, 2, 44100 * 2 + 1)
y = _triangle_stair(1, x)
plt.plot(x, y)
plt.show()