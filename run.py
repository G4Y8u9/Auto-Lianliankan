import metching
import cv2
import numpy as np
import win32api
import win32gui
import win32con
from PIL import ImageGrab
import time
from config import *
import numpy


def getGameWindowPosition():
    window = win32gui.FindWindow(None, WINDOW_TITLE)
    while not window:
        print('unable to find window, try in 3 secs...')
        time.sleep(3)
        window = win32gui.FindWindow(None, WINDOW_TITLE)
    win32gui.SetForegroundWindow(window)
    pos = win32gui.GetWindowRect(window)
    print("Window found at:" + str(pos))
    return pos[0], pos[1]


def getScreenImage():
    print('capturing screenshot...')
    scim = ImageGrab.grab()
    scim.save('screen.png')
    return cv2.imread("screen.png")


def getAllSquare(screen_image, game_pos):
    print('cutting pics...')
    game_x = game_pos[0] + MARGIN_LEFT
    game_y = game_pos[1] + MARGIN_HEIGHT
    all_square = []
    for x in range(0, H_NUM):
        for y in range(0, V_NUM):
            square = screen_image[game_y + y*SQUARE_HEIGHT:
                                  game_y + (y+1)*SQUARE_HEIGHT,
                                  game_x + x*SQUARE_WIDTH:
                                  game_x + (x+1)*SQUARE_WIDTH]
            all_square.append(square)
    return list(map(lambda square:
                    square[SUB_LT_Y:SUB_RB_Y, SUB_LT_X:SUB_RB_X], all_square))


def isImageExist(img, img_list):
    for existed_img in img_list:
        b = np.subtract(existed_img, img)
        if not np.any(b):
            return True
        else:
            continue
    return False


def getAllSquareTypes(all_square):
    print("sorting pics...")
    types = []
    empty_img = cv2.imread('empty.png')
    types.append(empty_img)
    for square in all_square:
        if not isImageExist(square, types):
            types.append(square)
    return types


all_avail_count = 0


def getAllSquareRecord(all_square_list, types):
    print("turning pics to matrix...")
    record = []
    line = []
    for square in all_square_list:
        num = 0
        for type in types:
            res = cv2.subtract(square, type)
            if not np.any(res):
                line.append(num)
                break
            num += 1

        if len(line) == V_NUM:
            record.append(line)
            line = []
    print(record)
    record_numpy = numpy.array(record, dtype=numpy.int16)
    global all_avail_count
    for each in record_numpy.reshape(-1):
        if each != 0:
            all_avail_count += 1
    all_avail_count = all_avail_count / 2
    print('%d pairs found' % all_avail_count)
    return record


def autoRelease(result, game_x, game_y, num, all_):
    for i in range(0, len(result)):
        for j in range(0, len(result[0])):
            if result[i][j] != 0:
                for m in range(0, len(result)):
                    for n in range(0, len(result[0])):
                        if result[m][n] != 0:
                            if metching.canConnect(i, j, m, n, result):
                                result[i][j] = 0
                                result[m][n] = 0
                                x1 = game_x + j*SQUARE_WIDTH
                                y1 = game_y + i*SQUARE_HEIGHT
                                x2 = game_x + n*SQUARE_WIDTH
                                y2 = game_y + m*SQUARE_HEIGHT
                                win32api.SetCursorPos((x1 + 15, y1 + 18))
                                win32api.mouse_event(
                                    win32con.MOUSEEVENTF_LEFTDOWN, x1+15,
                                    y1+18, 0, 0)
                                win32api.mouse_event(
                                    win32con.MOUSEEVENTF_LEFTUP, x1+15,
                                    y1+18, 0, 0)
                                ti = TIME_INTERVAL_1()
                                time.sleep(ti)
                                print('\tdelay 1：%.3f' % ti, end='')
                                win32api.SetCursorPos((x2 + 15, y2 + 18))
                                win32api.mouse_event(
                                    win32con.MOUSEEVENTF_LEFTDOWN, x2 + 15,
                                    y2 + 18, 0, 0)
                                win32api.mouse_event(
                                    win32con.MOUSEEVENTF_LEFTUP, x2 + 15,
                                    y2 + 18, 0, 0)
                                ti = TIME_INTERVAL(num/all_)
                                time.sleep(ti)
                                print('\tdelay 2：%.3f' % ti)
                                return True
    return False


def autoRemove(squares, game_pos):
    game_x = game_pos[0] + MARGIN_LEFT
    game_y = game_pos[1] + MARGIN_HEIGHT
    for i in range(0, int(all_avail_count)):
        print('Pair %d\tRemain %d\t' % ((i+1), all_avail_count-i-1), end='')
        autoRelease(squares, game_x, game_y, all_avail_count-i, all_avail_count)


if __name__ == '__main__':
    game_pos = getGameWindowPosition()
    time.sleep(1)
    screen_image = getScreenImage()
    all_square_list = getAllSquare(screen_image, game_pos)
    types = getAllSquareTypes(all_square_list)
    result = np.transpose(getAllSquareRecord(all_square_list, types))
    autoRemove(result, game_pos)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
