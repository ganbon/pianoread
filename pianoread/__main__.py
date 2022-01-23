import sys
import re
from pianoread.player import synthesizer

if __name__ == '__main__':
    args = sys.argv
    if 2 <= len(args):
        synthesizer(re.sub(r"^.*[/\\]|\.[^.]+", "", args[1]))
    else:
        print("引数が不足（入力ファイル名を指定してください）")