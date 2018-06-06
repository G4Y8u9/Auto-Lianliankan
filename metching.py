
__author__ = 'Threedog, G4Y8u9'
__Date__ = '2018/6/6 15:25'


result = None


def canConnect(x1, y1, x2, y2, r):
    global result
    result = r
    if result[x1][y1] == 0 or result[x2][y2] == 0:
        return False
    if x1 == x2 and y1 == y2:
        return False
    if result[x1][y1] != result[x2][y2]:
        return False
    if horizontalCheck(x1, y1, x2, y2):
        return True
    if verticalCheck(x1, y1, x2, y2):
        return True
    if turnOnceCheck(x1, y1, x2, y2):
        return True
    if turnTwiceCheck(x1, y1, x2, y2):
        return True
    return False


def horizontalCheck(x1, y1, x2, y2):
    global result
    if x1 == x2 and y1 == y2:
        return False
    if x1 != x2:
        return False
    startY = min(y1, y2)
    endY = max(y1, y2)
    if (endY - startY) == 1:
        return True
    for i in range(startY+1, endY):
        if result[x1][i] != 0:
            return False
    return True


def verticalCheck(x1, y1, x2, y2):
    global result
    if x1 == x2 and y1 == y2:
        return False
    if y1 != y2:
        return False
    startX = min(x1, x2)
    endX = max(x1, x2)
    if (endX - startX) == 1:
        return True
    for i in range(startX+1, endX):
        if result[i][y1] != 0:
            return False
    return True


def turnOnceCheck(x1, y1, x2, y2):
    global result
    if x1 == x2 and y1 == y2:
        return False
    if x1 != x2 and y1 != y2:
        cx, cy, dx, dy = x1, y2, x2, y1
        if result[cx][cy] == 0:
            if horizontalCheck(x1, y1, cx, cy) \
                    and verticalCheck(cx, cy, x2, y2):
                return True
        if result[dx][dy] == 0:
            if verticalCheck(x1, y1, dx, dy) \
                    and horizontalCheck(dx, dy, x2, y2):
                return True
    return False


def turnTwiceCheck(x1, y1, x2, y2):
    global result
    if x1 == x2 and y1 == y2:
        return False
    for i in range(0, len(result)):
        for j in range(0, len(result[1])):
            if result[i][j] != 0:
                continue
            if i != x1 and i != x2 and j != y1 and j != y2:
                continue
            if (i == x1 and j == y2) or (i == x2 and j == y1):
                continue
            if turnOnceCheck(x1, y1, i, j) and (horizontalCheck(i, j, x2, y2)
                                                or verticalCheck(i, j, x2, y2)):
                return True
            if turnOnceCheck(i, j, x2, y2) and (horizontalCheck(x1, y1, i, j)
                                                or verticalCheck(x1, y1, i, j)):
                return True
    return False
