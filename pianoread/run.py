import eel
import sys
import re

import player as ply

def test():
    eel.init("view", allowed_extensions=['.js', '.html', '.css'])
    eel.start("html/editor.html", block=False)

    args = sys.argv
    if 2 <= len(args):
        ply.synthesizer(re.sub(r"^.*[/\\]|\.[^.]+$", "", args[1]))
    else:
        print("引数が不足（入力ファイル名を指定してください）")
    
    while True:
        print("ok")
        eel.sleep(1.0)