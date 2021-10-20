import staff_notation as stf
import cv2
import numpy as np
import math
from scipy import ndimage

def count_dot(img, w, y1, y2):
  count = 0
  lists = []
  for num in range(w):
    for num2 in range(y1, y2 + 1):
      if img.item(num2, num) == 0:
        count += 1
    lists.append(count)
    count = 0

  return lists


def extract_lines(img, data):
  h, w = img.shape[:2]
  lists = []
  tmp = []
  bar_line = []

  for g in data:
    y1 = int(g[0][0][0] - (g[0][0][1] - 1) / 2)
    y2 = int(g[-1][-1][0] + (g[-1][-1][1] - 1) / 2)
    result = count_dot(img, w, y1, y2)
    lists.append(result)

    for index, item in enumerate(result):
      top_flg = bottom_flg = 0
      if item > (y2 - y1) * 0.925:
        for i in range(1, 7):
          if img.item(y1 - i, index) == 255:
            top_flg += 1
          if img.item(y2 + i, index) == 255:
            bottom_flg += 1

        if top_flg >= 3 and bottom_flg >= 3:
          tmp.append(index)

    bar_line.append(tmp)
    tmp = []

  return bar_line, lists


def data_shaping(data):
  shaped_data = []
  tmp = []
  for index, item in enumerate(data):
    if index == len(data) - 1 or item + 1 != data[index + 1]:
      tmp.append(item)
      mean = np.mean(tmp)
      weight = len(tmp)
      shaped_data.append([mean, weight])
      tmp = []
    else:
      tmp.append(item)

  return shaped_data


def draw_info(img, bar_line, data, lists):
  h, w = img.shape[:2]
  rgb_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
  rgb_img2 = rgb_img.copy()

  for idx, g in enumerate(data):
    y1 = int(g[0][0][0] - (g[0][0][1] - 1) / 2)
    for x in range(w):
      y2 = lists[idx][x] + y1
      rgb_img = cv2.line(rgb_img, (x, y1), (x, y2), (0, 0, 255), 1)
      if x in bar_line[idx]:
        y3 = int(g[-1][-1][0] + (g[-1][-1][1] - 1) / 2)
        rgb_img2 = cv2.line(rgb_img2, (x, y1), (x, y3), (0, 0, 255), 1)

  cv2.imwrite('data/dst/vertical_qty.jpg', rgb_img)
  cv2.imwrite('data/dst/bar_line.jpg', rgb_img2)
