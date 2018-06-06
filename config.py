# -*- coding:utf-8 -*-
__author__ = 'Threedog, G4Y8u9'
__Date__ = '2018/6/6 15:25'
import random


def TIME_INTERVAL(progress):
    return 0.375+random.uniform(-0.075, 0.075)+0.13*progress
    # return 0.001


def TIME_INTERVAL_1():
    return 0.375+random.uniform(-0.075, 0.075)
    # return 0.001


WINDOW_TITLE = "QQ游戏 - 连连看角色版"
MARGIN_LEFT = 14
MARGIN_HEIGHT = 181
H_NUM = 19
V_NUM = 11
SQUARE_WIDTH = 31
SQUARE_HEIGHT = 35
SUB_LT_X = 4
SUB_LT_Y = 4
SUB_RB_X = 25
SUB_RB_Y = 29
