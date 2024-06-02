import cv2
from texts import *
import os
from colorama import Fore, Back, Style, init; init()


fors  = [Fore.BLACK, Fore.BLUE, Fore.GREEN, Fore.CYAN, Fore.RED, Fore.MAGENTA, Fore.YELLOW, Fore.WHITE]
backs = [Back.BLACK, Back.BLUE, Back.GREEN, Back.CYAN, Back.RED, Back.MAGENTA, Back.YELLOW, Back.WHITE]
styles = [Style.NORMAL, Style.BRIGHT]
symbols = " ░▒▓"
# symbols = "▁▂▃▄▅▆▇█"



def clear(error_message):
  print(error_message)
  os.system("pause")
  os.system("cls")
  print(TITLE)


def read_action(actions, text):
  while True:
    action = input(text)
    if action == "$exit":
      exit()
    if action == "$home":
      return None
    try:
      action = int(action)
      if action in actions:
        return action
      else:
        clear(WRONG_ACTION__INCORRECT_NUMBER.format(action))
    except ValueError:
      clear(WRONG_ACTION__NOT_A_NUMBER)


def read_int(text):
  while True:
    number = input(text)
    if number == "$exit":
      exit()
    if number == "$home":
      return None
    try:
      number = int(number)
      return number
    except ValueError:
      print(WRONG_INT__NOT_A_NUMBER)


def read_normal_image_action():
  os.system("cls")
  print(TITLE)
  image = try_to_load_image()
  if image is None:
    print(READ_NORMAL_IMAGE_ACTION_GOBACK)
    os.system("pause")
    return
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  image = read_normal_image_action__resizing(image)
  if image is None:
    print(READ_NORMAL_IMAGE_ACTION_GOBACK)
    os.system("pause")
    return
  print(READ_NOMRAL_IMAGE_ACTION_STAGE_3)
  text, code = generate_text_image_from_normal_image(image)
  print(READ_NORMAL_IMAGE_ACTION_STAGE_4)
  os.system("pause")
  os.system("cls")
  print(text)
  os.system("pause")
  save = input(READ_NORMAL_IMAGE_ACTION_STAGE_5)
  if save.lower() == "y":
    with open("encoded_image.txt", "w", encoding="utf8") as f:
      f.write(code)
    print("Done!")
  os.system("pause")


def try_to_load_image():
  while True:
    try:
      filename = input(READ_NORMAL_IMAGE_ACTION_STAGE_1)
      if filename == "$home":
        break
      image = cv2.imread(filename)
      return image
    except Exception as e:
      clear(e, "Try again!")
  return None


def read_normal_image_action__resizing(image_rgb):
  action = read_action(range(1, 5), READ_NORMAL_IMAGE_ACTION_STAGE_2)
  match action:
    case 1:
      height, width, channels = image_rgb.shape
      new_width = read_int(READ_NORMAL_IMAGE_ACTION_STAGE_2_1)
      if new_width is None: return None
      return cv2.resize(image_rgb, (new_width, round(new_width * height / width / 2)))
    case 2:
      height, width, channels = image_rgb.shape
      new_height = read_int(READ_NORMAL_IMAGE_ACTION_STAGE_2_2)
      if new_height is None: return None
      return cv2.resize(image_rgb, (round(2 * new_height * width / height), new_height))
    case 3:
      return cv2.resize(image_rgb, (120, 30))
    case 4:
      return image_rgb


def generate_text_image_from_normal_image(image):
  text = ""
  code = []
  for row in image:
    for char in row:
      char, c = generate_symbol_by_color(char)
      text += char
      code.append(c)
    text += Style.RESET_ALL + "\n"
  
  code_text = ""
  
  for i in range(0, len(code), 2):
    if i != len(code) - 1:
      char = code[i] * 2 ** 10 + code[i+1]
      code_text += chr(char)
    else:
      code_text += chr(code[i] * 2**10)
  
  height, width, channels = image.shape
  width = chr(width)
  return text, code_text + width


def generate_symbol_by_color(char):
  # RGB
  # 000 - black
  # 001 - blue
  # 010 - green
  # 011 - cyan
  # 100 - red
  # 101 - magenta
  # 110 - yellow
  # 111 - white
  
  r, g, b = char[0] / 128, char[1] / 128, char[2] / 128
  fr, fg, fb = r, g, b
  br, bg, bb = r -.5, g -.5, b -.5
  
  fore = int(fr) * 4 + int(fg) * 2 + int(fb)
  back = int(br) * 4 + int(bg) * 2 + int(bb)
  
  style = max([r % .5, g % .5, b % .5]) > .25
  symbol = int(max([r, g, b]) * len(symbols) / 2)
  
  char = fors[fore] + backs[back] + styles[style] + symbols[symbol]
  
  # Code:
  # Fore  Style
  # 0001110111 Symbol
  #    Back
  code = fore * 2 ** 7 + back * 2 ** 4 + style * 2 ** 3 + symbol
  
  return char, code


def read_code_action():
  print(DECODE_IMAGE_STAGE_1)
  os.system("pause")
  print(DECODE_IMAGE_STAGE_2)
  with open("image_to_decode.txt", encoding="utf-8") as f:
    ft = f.read()
    if ft.endswith('\n'): ft = ft[:-1]
    text, width = decode_image(ft)
    print(DECODE_IMAGE_STAGE_3.format(width))
    os.system("pause")
    print(text)
    print(Style.RESET_ALL)
    os.system("pause")


def decode_image(code):
  res = []
  for i in range(len(code)-1):
    char = code[i]
    number = ord(char)
    left = number // 2**10
    right = number % 2**10
    res += [left, right]
  width = ord(code[-1])
  
  text = ""
  i = 0
  for char in res:
    fore = char // 2 ** 7
    char %= 2 ** 7
    back = char // 2 ** 4
    char %= 2 ** 4
    style = char // 2 ** 3
    char %= 2 ** 3
    symbol = char
    
    try:
      text += fors[fore] + backs[back] + styles[style] + symbols[symbol]
    except:
      print(f"{char=} {fore=} {back=} {style=} {symbol=}")
    i += 1
    if i >= width:
      text += Style.RESET_ALL + '\n'
      i = 0
  return text, width


def main():
  while True:
    os.system("cls")
    print(TITLE)
    action = read_action(range(1,3), MAIN_PAGE)
    match action:
      case 1:
        read_normal_image_action()
      case 2:
        read_code_action()


if __name__ == "__main__":
  main()
