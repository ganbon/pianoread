from typing import overload
import cv2
import math
import numpy as np
from PIL import Image, ImageDraw


def get_count(im, weight_lists, x, score_list):
  count = 0

  for idx, k in enumerate(weight_lists):
    if im.getpixel((x, k)) == 0:
      count += score_list[idx]

  return count


def judge_alone(im, x, top, bottom, limit):
  if top >= limit[0] and bottom <= limit[1] and im.getpixel((x, top)) == 255 and im.getpixel((x, bottom)) == 255:
    return True
  else:
    return False


def remove_h_line(im, w, min_l, y, weight, draw):
  overflow = 1
  point = w // 2
  lists = []
  tmp = []
  weight_lists = range(int(y - (weight - 1) / 2  - overflow), int(y + (weight - 1) / 2 + overflow) + 1)
  length = len(weight_lists)
  score_list = [0] * length
  limit = [math.ceil(y - weight - overflow) - 1, math.floor(y + weight + overflow) + 1]
  
  for i in range(-(-length // 2)): # 切り上げ
    score_list[i] = i + 1
    score_list[-(i + 1)] = i + 1

  for i in [-1, 1]:
    top = int(y - (weight - 1) / 2 - overflow - 1)
    bottom = int(y + (weight - 1) / 2 + overflow + 1)
    py = t_py =y
    t_top = top
    t_bottom = bottom
    for j in range(point):
      x = point + (i * j)
      count = get_count(im, weight_lists, x, score_list)
      upper = list(map(lambda n: n - 1, weight_lists))
      lower = list(map(lambda n: n + 1, weight_lists))
      middle_judge = judge_alone(im, x, top, bottom, limit)
      upper_judge = judge_alone(im, x, top - 1, bottom - 1, limit)
      lower_judge = judge_alone(im, x, top + 1, bottom + 1, limit)
      upper_count = get_count(im, upper, x, score_list)
      lower_count = get_count(im, lower, x, score_list)

      if not len(tmp):
        t_py = py
        t_top = top
        t_bottom = bottom

      if middle_judge:
        if upper_judge and lower_judge and upper_count > count and lower_count > count:
          if upper_count > lower_count:
            py -= 1
            top -= 1
            bottom -= 1
            weight_lists = upper.copy()
            tmp.append([x, py])
          else:
            py += 1
            top += 1
            bottom += 1
            weight_lists = lower.copy()
            tmp.append([x, py])
        elif upper_judge and upper_count > count:
          py -= 1
          top -= 1
          bottom -= 1
          weight_lists = upper.copy()
          tmp.append([x, py])
        elif lower_judge and lower_count > count:
          py += 1
          top += 1
          bottom += 1
          weight_lists = lower.copy()
          tmp.append([x, py])
        else:
          tmp.append([x, py])

      else:
        if upper_judge and lower_judge and upper_count > lower_count:
          py -= 1
          top -= 1
          bottom -= 1
          weight_lists = upper.copy()
          tmp.append([x, py])
        elif upper_judge:
          py -= 1
          top -= 1
          bottom -= 1
          weight_lists = upper.copy()
          tmp.append([x, py])
        elif lower_judge:
          py += 1
          top += 1
          bottom += 1
          weight_lists = lower.copy()
          tmp.append([x, py])
        else:
          if len(tmp) > min_l:
            lists.extend(tmp)
          else:
            py = t_py
            top = t_top
            bottom = t_bottom
          tmp.clear()

    if len(tmp) > min_l:
      lists.extend(tmp)
    
    tmp.clear()

  for item in lists:
    top = int(item[1] - (weight - 1) / 2 - overflow)
    bottom = int(item[1] + (weight - 1) / 2 + overflow)
    draw.line(((item[0], top), (item[0], bottom)), width=1, fill= 128)


def remove_v_line(im, yt, yb, min_l, x, weight, draw):
  bold = {1:2, 2:2, 3:2, 4:2, 5:2}
  overflow = bold[weight]
  left = int(x - (weight - 1) / 2 - overflow)
  right = int(x + (weight - 1) / 2 + overflow)
  y1 = y2 = -1

  for y in range(yt, yb + 1):
    if im.getpixel((left, y)) == 255 and im.getpixel((right, y)) == 255:
      if y1 == -1:
        y1 = y
      y2 = y
    elif y2 - y1 >= min_l:
      draw.line(((x, y1), (x, y2)), width= weight + 2 * overflow, fill= 255)
      y1 = y2 = -1
    else:
      y1 = y2 = -1

  if y2 - y1 >= min_l:
    draw.line(((x, y1), (x, y2)), width= weight + 2 * overflow, fill= 255)


def extract_obj(img, staff_notation, bar_line, line_pitch):
  im = Image.fromarray(img) # モードはL
  draw = ImageDraw.Draw(im)
  w, h = im.size
  min_length = w // 140
  min_length_v = line_pitch / 3
  print(min_length)

  for idx, item in enumerate(bar_line):
    g = staff_notation[idx]
    yt = int(g[0][0][0] - (g[0][0][1] - 1) / 2)
    yb = int(g[-1][-1][0] + (g[-1][-1][1] - 1) / 2)
    for item2 in item:
      remove_v_line(im, yt, yb, min_length_v, item2[0], item2[1], draw)

  im2 = im.copy()
  draw2 = ImageDraw.Draw(im2)

  for item in staff_notation:
    for item2 in item:
      for item3 in item2:
        remove_h_line(im, w * 2 // 3, min_length, item3[0], item3[1], draw)
        remove_h_line(im2, w, min_length, item3[0], item3[1], draw2)

  left = w // 2 - min_length * 4
  right = w // 2 + min_length * 4
  im_crop = im.crop((left, 0, right, h))

  im2.paste(im_crop, (left, 0))

  img_dst = np.array(im2)

  return img_dst
