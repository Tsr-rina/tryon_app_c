import numpy as np
import cv2


def makecounter(path):
  # カーネルを定義
  kernel = np.ones((5,5), np.uint8)
  kernel[0,0] = kernel[0,4] = kernel[4,0] = kernel[4,4] = 0
  # gray = cv2.imread(path, cv2MREAD_GRAYSCALE)
  img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
  # if img.shape[2] == 4:
  #   mask = img[:,:,3] == 0
  #   img[mask] = [255] * 4
  #  img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
  gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
  # ノイズ除去
  # gray = cv2.fastNlMeansDenoising(gray, h=10)
  # 白い部分を膨張させる
  dilated = cv2.dilate(gray, kernel, iterations=1)
  # 差分をとる
  diff = cv2.absdiff(dilated, gray)
  # 白黒反転して2値化
  contour = cv2.adaptiveThreshold(255 - diff, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 8)
  return contour