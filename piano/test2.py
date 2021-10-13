from pydub import AudioSegment
from pydub import effects
from playsound import playsound

# 曲の読み込み
af = AudioSegment.from_mp3("1-3.mp3")

# 曲のスピードを倍に設定
af2 = af.speedup(playback_speed=2.0, crossfade=0)

# 曲を保存する
playsound("1-3.mp3")