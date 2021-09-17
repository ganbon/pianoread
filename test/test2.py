import cv2
import numpy as np
import math
import sys
from scipy import ndimage
from scipy.signal import argrelmax
from PIL import Image
import matplotlib.pyplot as plt


def get_degree(img, rgb_img):
  _, img_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
  reverse_img = cv2.bitwise_not(img_otsu)
  h, w = img_otsu.shape[:2]
  minLineLength = w // 3
  maxLineGap = w // 5
  lines = cv2.HoughLinesP(reverse_img, 1, np.pi/360, 100, minLineLength, maxLineGap)

  sum_arg = 0
  count = 0
  for line in lines:
    for x1, y1, x2, y2 in line:
      arg = math.degrees(math.atan2((y2-y1), (x2-x1)))
      HORIZONTAL = 0
      DIFF = 10 # 許容誤差 -> -10 - +10 を本来の水平線と考える
      if arg > HORIZONTAL - DIFF and arg < HORIZONTAL + DIFF :
        rgb_img = cv2.line(rgb_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        sum_arg += arg
        count += 1
  if count == 0:
    return HORIZONTAL
  else:
    return (sum_arg / count) - HORIZONTAL


def count_dot(img, r):
  count = 0
  for num in range(W):
    if img.item(r, num) == 0:
      count += 1
  return count


def gen_graph(img):
  lists = []
  for r in range(H):
    lists.append(count_dot(img, r))

  staff_notation = [index for index, item in enumerate(lists) if item > W // 2]

  rgb_img2 = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
  rgb_img3 = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
  for y in staff_notation:
    rgb_img2 = cv2.line(rgb_img2, (0, y), (W, y), (0, 0, 255), 1)

  cv2.imwrite('data/dst/test3.jpg', rgb_img2)

  for index, qty in enumerate(lists):
    rgb_img3 = cv2.line(rgb_img3, (0, index), (qty, index), (0, 0, 255), 1)
  cv2.imwrite('data/dst/test4.jpg', rgb_img3)

  return staff_notation, lists


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


def meas_distance(data):
  dist_lists = [0] * H * 2
  for index in range(len(data) - 1):
    dist_lists[int((data[index + 1][0] - data[index][0]) * 2)] += 1

  max_val = max(dist_lists)
  result = [idx for idx, item in enumerate(dist_lists) if item == max_val]

  return np.mean(result) / 2


def grouping_staff_notation(data):
  dist_basis = meas_distance(data)
  print(dist_basis)
  result = []
  tmp = [data[0]]

  for index in range(1, len(data)):
    if abs(data[index][0] - data[index - 1][0] - dist_basis) <= 1.5:
      tmp.append(data[index])
    else:
      result.append(tmp)
      tmp = [data[index]]

  result.append(tmp)
  return result, dist_basis


def draw_staff_notation(data, img):
  rgb_img5 = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

  lists1 = []
  lists2 = []
  lists3 = []
  for item in data:
    l = len(item)
    if l == 5:
      lists1.append(item)
    elif 1 < l:
      lists2.append(item)
    else:
      lists3.append(item)
  # lists2 = [item for item in data if 1 < len(item) < 5]

  for item in lists1:
    for item2 in item:
       rgb_img5 = cv2.line(rgb_img5, (0, int(item2[0])), (W, int(item2[0])), (0, 0, 255), item2[1])

  for item in lists2:
    for item2 in item:
       rgb_img5 = cv2.line(rgb_img5, (0, int(item2[0])), (W, int(item2[0])), (0, 255, 0), item2[1])

  for item in lists3:
    for item2 in item:
       rgb_img5 = cv2.line(rgb_img5, (0, int(item2[0])), (W, int(item2[0])), (255, 0, 0), item2[1])

  cv2.imwrite('data/dst/test5.jpg', rgb_img5)


# 画像の読み込み
img = cv2.imread("./data/Original_Score/0003.jpg", 0)
rgb_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

arg = get_degree(img, rgb_img)
print("arg: {}".format(arg))
img = ndimage.rotate(img, arg, cval=255)
ret, img_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
H, W = img_otsu.shape[:2]

staff_notation_opts1, hrizontal_length = gen_graph(img_otsu)
staff_notation_opts2 = data_shaping(staff_notation_opts1)

staff_notation_opts3, distance = grouping_staff_notation(staff_notation_opts2)
print(staff_notation_opts3)

draw_staff_notation(staff_notation_opts3, img_otsu)

#閾値がいくつになったか確認
print("ret: {}\n{}×{}".format(ret, W, H))

cv2.imwrite('data/dst/test1.jpg', img_otsu)
cv2.imwrite('data/dst/test2.jpg', rgb_img)