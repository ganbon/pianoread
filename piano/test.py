from playsound import playsound
text=input()
text=list(text)
for i in range(len(text)):
    if(text[i]=='ド'):
        playsound('1-1.mp3')
    elif(text[i]=='レ'):
        playsound('1-2.mp3')
    elif(text[i]=='ミ'):
        playsound('1-3.mp3')
    elif(text[i]=='フ'):
        playsound('1-4.mp3')
    elif(text[i]=='ソ'):
        playsound('1-5.mp3')
    elif(text[i]=='ラ'):
        playsound('1-6.mp3')
    elif(text[i]=='シ'):
        playsound('1-7.mp3')