import win32gui
import win32con
import win32api
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time

def add_text(img, text, left, top, textColor=(0, 0, 0), textSize=20):
	img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
	draw = ImageDraw.Draw(img)
	fontStyle = ImageFont.truetype("font/msyh.ttc", textSize, encoding="utf-8")
	draw.text((left, top), text, textColor, font=fontStyle)
	return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

def make_window_borderless(hwnd):	
	style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
	style &= ~win32con.WS_OVERLAPPEDWINDOW
	style |= win32con.WS_POPUP
	win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
	win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
	win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

def get_title_bar_height(hwnd):
	_, top, _, bottom = win32gui.GetWindowRect(hwnd)
	_, _, _, a_bottom = win32gui.GetClientRect(hwnd)
	return bottom - a_bottom - top

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

background = cv2.imread("./background.png")
ys_hwnd = win32gui.FindWindow(None, "原神")
cv2.imshow("mask", np.ones((1, 1, 3), np.uint8) * 255)
mask_hwnd = win32gui.FindWindow(None, "mask")
make_window_borderless(mask_hwnd)
pop_window("原神")
img = None
t = time.time()
left = top = right = bottom = ratio = None
while (time.time() - t) <= 60:
	if (left, top, right, bottom) != win32gui.GetWindowRect(ys_hwnd):
		left, top, right, bottom = win32gui.GetWindowRect(ys_hwnd)
		tb_height = get_title_bar_height(ys_hwnd)
		bottom -= tb_height
	if ratio != (right - left) / (bottom - top):
		ratio = (right - left) / (bottom - top)
		if ratio <= background.shape[1] / background.shape[0]:
			img = cv2.resize(background, (0, 0), fx=(bottom - top) / background.shape[0], fy=(bottom - top) / background.shape[0], interpolation=cv2.INTER_AREA)[0:(bottom - top), 0:(right - left), :]
		else:
			img = cv2.resize(background, (0, 0), fx=(right - left) / background.shape[1], fy=(right - left) / background.shape[1], interpolation=cv2.INTER_AREA)[0:(bottom - top), 0:(right - left), :]
	font_size = int((bottom - top) / 7.5)
	mask = add_text(img, "距离游戏开始还有" + str(int(60 + t - time.time())) + "秒", 10, (bottom - top) // 2 - font_size // 2, (115, 201, 229), font_size)
	cv2.imshow("mask", mask)
	cv2.moveWindow('mask', left, top + tb_height)
	win32gui.ShowWindow(mask_hwnd, win32con.SW_SHOWNORMAL)
	win32gui.SetWindowPos(mask_hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
	cv2.waitKey(1)
	time.sleep(0.05)
t = time.time()
left = top = right = bottom = None
while (time.time() - t) <= 180:
	if (left, top, right, bottom) != win32gui.GetWindowRect(ys_hwnd):
		left, top, right, bottom = win32gui.GetWindowRect(ys_hwnd)
		tb_height = get_title_bar_height(ys_hwnd)
		bottom -= tb_height
		side = int((bottom - top) / 5.5)
		img = np.ones((side, side, 3), np.uint8) * 255
	mask = img.copy()
	font_size = int(side / 7.5)
	mask = add_text(img, "距离限制解除", 10, side // 2 - font_size // 2, (251, 114, 153), font_size)
	mask = add_text(mask, "还有" + str(int(180 + t - time.time())) + "秒", 10, side // 2 + font_size // 2, (251, 114, 153), font_size)
	cv2.imshow("mask", mask)
	cv2.moveWindow("mask", left + (right - left) // 40, top + tb_height)
	win32gui.ShowWindow(mask_hwnd, win32con.SW_SHOWNORMAL)
	win32gui.SetWindowPos(mask_hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
	cv2.waitKey(1)
	time.sleep(0.05)
cv2.imshow("mask", np.ones((1, 1, 3), np.uint8) * 255)
time.sleep(5)
t = time.time()
while (time.time() - t) <= 60:
	if (left, top, right, bottom) != win32gui.GetWindowRect(ys_hwnd):
		left, top, right, bottom = win32gui.GetWindowRect(ys_hwnd)
		tb_height = get_title_bar_height(ys_hwnd)
		bottom -= tb_height
		side = int((bottom - top) / 5.5)
		img = np.ones((side, side, 3), np.uint8) * 255
	mask = img.copy()
	font_size = int(side / 7.5)
	mask = add_text(img, "距离游戏结束", 10, side // 2 - font_size // 2, (251, 114, 153), font_size)
	mask = add_text(mask, "还有" + str(int(60 + t - time.time())) + "秒", 10, side // 2 + font_size // 2, (251, 114, 153), font_size)
	cv2.imshow("mask", mask)
	cv2.moveWindow("mask", left + (right - left) // 40, top + tb_height)
	win32gui.ShowWindow(mask_hwnd, win32con.SW_SHOWNORMAL)
	win32gui.SetWindowPos(mask_hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
	cv2.waitKey(1)
	time.sleep(0.05)
cv2.destroyAllWindows()