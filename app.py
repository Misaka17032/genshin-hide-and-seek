import win32gui
import win32con
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time

def add_text(img, text, left, top, textColor=(0, 0, 0), textSize=20):
	img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
	draw = ImageDraw.Draw(img)
	fontStyle = ImageFont.truetype("font/simsun.ttc", textSize, encoding="utf-8")
	draw.text((left, top), text, textColor, font=fontStyle)
	return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

def pop_window(name):
	handle = win32gui.FindWindow(0, name)
	if handle == 0:
		return False
	else:
		win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
		win32gui.SetForegroundWindow(handle)
		while (win32gui.IsIconic(handle)):
			continue
		return True

pop_window("原神")
t = time.time()
while (time.time() - t) <= 60:
	ys_hwnd = win32gui.FindWindow(None, "原神")
	left, top, right, bottom = win32gui.GetWindowRect(ys_hwnd)
	img = np.ones((bottom - top, right - left, 3), np.uint8) * 255
	font_size = int((bottom - top) / 7.5)
	img = add_text(img, "距离游戏开始还有" + str(int(60 + t - time.time())) + "秒", 10, (bottom - top) // 2 - font_size // 2, (0, 0, 0), font_size)
	cv2.imshow("mask", img)
	mask_hwnd = win32gui.FindWindow(None, "mask")
	win32gui.ShowWindow(mask_hwnd, win32con.SW_SHOWNORMAL)
	win32gui.SetWindowPos(mask_hwnd, win32con.HWND_TOPMOST, left, top, 0, 0, win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
	cv2.waitKey(1)
t = time.time()
while (time.time() - t) <= 180:
	ys_hwnd = win32gui.FindWindow(None, "原神")
	left, top, right, bottom = win32gui.GetWindowRect(ys_hwnd)
	side = int((bottom - top) / 5.5)
	img = np.ones((side, side, 3), np.uint8) * 255
	if (time.time() - t) >= 120:
		font_size = int(side / 7.5)
		img = add_text(img, "距离限制解除", 10, side // 2 - font_size, (0, 0, 0), font_size)
		img = add_text(img, "还有" + str(int(180 + t - time.time())) + "秒", 10, side // 2 + font_size, (0, 0, 0), font_size)
	cv2.imshow("mask", img)
	mask_hwnd = win32gui.FindWindow(None, "mask")
	win32gui.ShowWindow(mask_hwnd, win32con.SW_SHOWNORMAL)
	win32gui.SetWindowPos(mask_hwnd, win32con.HWND_TOPMOST, left + (right - left) // 40, top, 0, 0, win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
	cv2.waitKey(1)
cv2.destroyAllWindows()
time.sleep(5)
t = time.time()
while (time.time() - t) <= 60:
	ys_hwnd = win32gui.FindWindow(None, "原神")
	left, top, right, bottom = win32gui.GetWindowRect(ys_hwnd)
	side = int((bottom - top) / 5.5)
	img = np.ones((side, side, 3), np.uint8) * 255
	img = add_text(img, "距离游戏结束", 10, side // 2 - font_size, (0, 0, 0), font_size)
	img = add_text(img, "还有" + str(int(60 + t - time.time())) + "秒", 10, side // 2 + font_size, (0, 0, 0), font_size)
	cv2.imshow("mask", img)
	mask_hwnd = win32gui.FindWindow(None, "mask")
	win32gui.ShowWindow(mask_hwnd, win32con.SW_SHOWNORMAL)
	win32gui.SetWindowPos(mask_hwnd, win32con.HWND_TOPMOST, left + (right - left) // 40, top, 0, 0, win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
	cv2.waitKey(1)
cv2.destroyAllWindows()