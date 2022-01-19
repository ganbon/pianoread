#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pretty_midi
from scipy.io import wavfile
from pathlib import Path

CURRENT_DIR = str(Path(__file__).resolve().parent)

def create_music():
    # 準備
    new_music = pretty_midi.PrettyMIDI()

    # チェロを設定
    cello_program = pretty_midi.instrument_name_to_program("Cello")
    cello = pretty_midi.Instrument(program=cello_program)

    # どれみふぁそらしどを鳴らす
    time = 0.0
    for note_name in ["C5", "D5", "E5", "F5", "G5", "A5", "B5", "C6"]:
        note_number = pretty_midi.note_name_to_number(note_name)
        note = pretty_midi.Note(
            velocity=100, pitch=note_number, start=time, end=(time + 0.5)
        )
        cello.notes.append(note)
        time = time + 0.5
    new_music.instruments.append(cello)

    # fuildsynthを使ってサウンドフォントを使ったデータに変換
    audio_data = new_music.fluidsynth(
        sf2_path=CURRENT_DIR + "/sf/GeneralUser GS v1.471.sf2"
    )
    filename = CURRENT_DIR + "/output/sample.wav"

    # wavで書き出し
    wavfile.write(filename, 44100, audio_data)

create_music()