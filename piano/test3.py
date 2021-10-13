from playsound import playsound
from multiprocessing import Process
mp1='1-1.mp3'
mp2='1-3.mp3'
mp3='1-5.mp3'
def sound1():
    playsound(mp1)

def sound2():
    playsound(mp2)

def sound3():
    playsound(mp3)

if __name__ == '__main__':
    p = Process(target=sound2)
    p.start()
    t=Process(target=sound3)
    t.start()
    sound1()
