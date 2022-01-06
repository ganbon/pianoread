from train.data_test import result_img
from note.note_scale import scale_disc


def note_set(path, img, coor):
    note_scale = None
    train_data = "../train_data/train_cnn_note.h5"
    note_kind = result_img(img, train_data)
    if  note_kind < 0:
        return [img, note_kind, note_scale]
    else:
        note_scale = scale_disc(path, coor, note_kind)
    print(img)
    return [img, note_kind, note_scale]


def data_unpack(notes):
    note_img = note_set(*notes)
    return note_img
