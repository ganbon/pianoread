def get_count(im, weight_lists, x):
  count = 0
  for k in weight_lists:
    if im.getpixel((x, k)) == 0:
      count += 1
  return count


def judge_alone(im, x, top, bottom):
  if im.getpixel((x, top)) == 255 and im.getpixel((x, bottom)) == 255:
    return True
  else:
    return False


def remove_h_line2(im, w, min_l, y, weight, draw):
  bold = {1:2, 2:2, 3:2, 4:2, 5:2}
  overflow = bold[weight]
  point = w // 2
  lists = []
  tmp = []
  weight_lists = range(int(y - (weight - 1) / 2), int(y + (weight - 1) / 2) + 1)

  for i in [-1, 1]:
    top = int(y - (weight - 1) / 2 - overflow)
    bottom = int(y + (weight - 1) / 2 + overflow)
    py = y
    for j in range(point):
      x = point + (i * j)
      if not judge_alone(im, x, top, bottom):
        if len(tmp) > min_l:
          lists.extend(tmp)
        tmp.clear()
        continue

      count = get_count(im, weight_lists, x)
      upper = map(lambda n: n - 1, weight_lists)
      upper_judge = judge_alone(im, x, top - 1, bottom - 1)
      lower = map(lambda n: n + 1, weight_lists)
      lower_judge = judge_alone(im, x, top + 1, bottom + 1)

      if get_count(im, upper, x) > count and upper_judge:
        py -= 1
        top -= 1
        bottom -= 1
        weight_lists = list(upper).copy()
        tmp.append([x, py])

      elif get_count(im, lower, x) > count and lower_judge:
        py += 1
        top += 1
        bottom += 1
        weight_lists = list(lower).copy()
        tmp.append([x, py])

      else:
        tmp.append([x, py])

    if len(tmp) > min_l:
      lists.extend(tmp)
    
    tmp.clear()

  for item in lists:
    top = int(item[1] - (weight - 1) / 2 - overflow)
    bottom = int(item[1] + (weight - 1) / 2 + overflow)
    draw.line(((item[0], top), (item[0], bottom)), width=1, fill= 255)