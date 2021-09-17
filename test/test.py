import cv2
import numpy as np
import math
import sys
from scipy import ndimage
from scipy.signal import argrelmax
from PIL import Image
import matplotlib.pyplot as plt

# 幅が指定した値になるように、アスペクト比を固定して、リサイズする。
# def scale_to_width(img, width):
#   h, w = img.shape[:2]
#   height = round(h * (width / w))
#   dst = cv2.resize(img, dsize=(width, height), interpolation=cv2.INTER_NEAREST)

#   return dst

def get_degree(img, rgb_img):
  _, img_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
  reverse_img = cv2.bitwise_not(img_otsu)
  h, w = img_otsu.shape[:2]
  # edges = cv2.Canny(img, 50, 150, apertureSize = 3)
  minLineLength = w // 3
  maxLineGap = w // 5
  print(minLineLength, maxLineGap)
  lines = cv2.HoughLinesP(reverse_img, 1, np.pi/360, 100, minLineLength, maxLineGap)

  sum_arg = 0
  count = 0
  for line in lines:
    for x1, y1, x2, y2 in line:
      rgb_img = cv2.line(rgb_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
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

# def draw_line(rgb_img, rotate_img):
#   reverse_img = cv2.bitwise_not(rotate_img)
#   minLineLength = 200
#   maxLineGap = 30
#   lines = cv2.HoughLinesP(reverse_img, 1, np.pi/360, 100, minLineLength, maxLineGap)

#   for line in lines:
#     for x1, y1, x2, y2 in line:
#       arg = math.degrees(math.atan2((y2-y1), (x2-x1)))
#       HORIZONTAL = 0
#       DIFF = 0.25 # 許容誤差 -> -10 - +10 を本来の水平線と考える
#       if arg > HORIZONTAL - DIFF and arg < HORIZONTAL + DIFF :
#         rgb_img = cv2.line(rgb_img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# 画像の読み込み
img = cv2.imread("./data/Original_Score/0001.jpg", 0)
rgb_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

arg = get_degree(img, rgb_img)
print("arg: {}".format(arg))
img = ndimage.rotate(img, arg, cval=255)
ret, img_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
h, w = img_otsu.shape[:2]

def count_dot(img, r):
  count = 0
  for num in range(w):
    if img.item(r, num) == 0:
      count += 1
  return count

def gen_graph(img):
  lists = []
  for r in range(h):
    lists.append(count_dot(img, r))

  staff_notation = [index for index, item in enumerate(lists) if item > w // 2]

  # staff_notation = argrelmax(np.array(lists), order = 8)

  # lists2 = []
  # for index in staff_notation[0]:
  #   lists2.append(lists[index])
  # staff_notation = np.vstack((staff_notation, np.array(lists2)))

  # lists2.sort(reverse=True)
  # threshold = lists2[9] * 0.6
  # tmp = []
  # for index, item in enumerate(staff_notation[1]):
  #   if item < threshold:
  #     tmp.append(index)
  # staff_notation = np.delete(staff_notation, tmp, 1)

  rgb_img2 = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
  rgb_img3 = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
  for y in staff_notation:
    rgb_img2 = cv2.line(rgb_img2, (0, y), (w, y), (0, 0, 255), 1)

  cv2.imwrite('data/dst/test3.jpg', rgb_img2)

  # x = range(150)
  # plt.bar(x, lists[750:900], width=1)
  # plt.savefig("hoge.png")
  for index, qty in enumerate(lists):
    rgb_img3 = cv2.line(rgb_img3, (0, index), (qty, index), (0, 0, 255), 1)
  cv2.imwrite('data/dst/test4.jpg', rgb_img3)
  

gen_graph(img_otsu)

# rgb_img = cv2.cvtColor(img_otsu, cv2.COLOR_GRAY2RGB)
# draw_line(rgb_img, img_otsu)

#閾値がいくつになったか確認
print("ret: {}\n{}×{}".format(ret, w, h))

#画像の確認
# cv2.imshow("otsu", rgb_img)
# cv2.waitKey()
# cv2.destroyAllWindows()

cv2.imwrite('data/dst/test1.jpg', img_otsu)
cv2.imwrite('data/dst/test2.jpg', rgb_img)