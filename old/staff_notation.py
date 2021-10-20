import cv2
import numpy as np
import math


def get_degree(img):
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
        sum_arg += arg
        count += 1
  if count == 0:
    return HORIZONTAL
  else:
    return (sum_arg / count) - HORIZONTAL


def count_dot(img, r, w):
  count = 0
  for num in range(w):
    if img.item(r, num) == 0:
      count += 1

  return count


def count_conse_dot(img, r, w):
  max = 0
  count = 0
  max_gap = 6
  gap = 0

  for num in range(w):
    if img.item(r, num) == 0:
      count += 1 + gap
      gap = 0
      if count > max:
        max = count
    else:
      gap += 1

    if gap > max_gap:
      count = 0
      gap = 0

  return max


def extract_lines(img):
  h, w = img.shape[:2]
  lists = []
  for r in range(h):
    lists.append(count_dot(img, r, w))

  staff_notation = [index for index, item in enumerate(lists) if item > w // 2]

  return staff_notation, lists


def extract_long_lines(img):
  h, w = img.shape[:2]
  lists = []
  for r in range(h):
    lists.append(count_conse_dot(img, r, w))

  stafff_notation = [index for index, item in enumerate(lists) if item > w // 3]

  return stafff_notation, lists


def extract_lines_H(img):
  reverse_img = cv2.bitwise_not(img)
  h, w = img.shape[:2]
  minLineLength = w // 3
  maxLineGap = w // 5

  lines = cv2.HoughLinesP(reverse_img, 1, np.pi/360, 100, minLineLength, maxLineGap)

  lines_list = []
  for line in lines:
    for x1, y1, x2, y2 in line:
      arg = math.degrees(math.atan2((y2-y1), (x2-x1)))
      HORIZONTAL = 0
      DIFF = 0.5 # 許容誤差
      if arg > HORIZONTAL - DIFF and arg < HORIZONTAL + DIFF :
        lines_list.append([x1, y1, x2, y2])

  return lines_list


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


def meas_distance(data, h):
  dist_lists = [0] * h * 2
  for index in range(len(data) - 1):
    dist_lists[int((data[index + 1][0] - data[index][0]) * 2)] += 1

  max_val = max(dist_lists)
  result = [idx for idx, item in enumerate(dist_lists) if item == max_val]

  return np.mean(result) / 2


def grouping_staff_notation(data, h):
  dist_basis = meas_distance(data, h)
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


def get_staff_notation(data):
  tmp = [item for item in data if len(item) == 5]
  lists = []
  for index in range(0, len(tmp), 2):
    lists.append([tmp[index], tmp[index + 1]])

  return lists


def draw_staff_notation(data, img):
  h, w = img.shape[:2]
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

  for item in lists1:
    for item2 in item:
       rgb_img5 = cv2.line(rgb_img5, (0, int(item2[0])), (w, int(item2[0])), (0, 0, 255), item2[1])

  for item in lists2:
    for item2 in item:
       rgb_img5 = cv2.line(rgb_img5, (0, int(item2[0])), (w, int(item2[0])), (0, 255, 0), item2[1])

  for item in lists3:
    for item2 in item:
       rgb_img5 = cv2.line(rgb_img5, (0, int(item2[0])), (w, int(item2[0])), (255, 0, 0), item2[1])

  cv2.imwrite('data/dst/staff_notation.jpg', rgb_img5)


def draw_info(img, img_otsu, lines_list, staff_notation, dot_list, line_list):
  rgb_img = cv2.cvtColor(img_otsu, cv2.COLOR_GRAY2RGB)
  rgb_img2 = rgb_img.copy()
  rgb_img3 = rgb_img.copy()
  rgb_img4 = rgb_img.copy()
  h, w = img_otsu.shape[:2]

  for x1, y1, x2, y2 in lines_list:
    rgb_img = cv2.line(rgb_img, (x1, y1), (x2, y2), (0, 0, 255), 1)
  cv2.imwrite('data/dst/horizontal_lines_H.jpg', rgb_img)

  for y in staff_notation:
    rgb_img2 = cv2.line(rgb_img2, (0, y), (w, y), (0, 0, 255), 1)
  cv2.imwrite('data/dst/horizontal_lines.jpg', rgb_img2)

  for index, qty in enumerate(dot_list):
    rgb_img3 = cv2.line(rgb_img3, (0, index), (qty, index), (0, 0, 255), 1)
  cv2.imwrite('data/dst/horizontal_qty.jpg', rgb_img3)

  for index, qty in enumerate(line_list):
    rgb_img4 = cv2.line(rgb_img4, (0, index), (qty, index), (0, 0, 255), 1)
  cv2.imwrite('data/dst/horizontal_long_qty.jpg', rgb_img4)


# 五線譜が欠損している場合、推測して埋め合わせるようにする予定
