import cv2
import numpy as np

# 水平方向投影
def hProject(binary):
    h, w = binary.shape
    # 水平投影
    hprojection = np.zeros(binary.shape, dtype=np.uint8)
    # 创建h长度都为0的数组
    h_h = [0]*h
    for j in range(h):
        for i in range(w):
            if binary[j,i] == 0:
                h_h[j] += 1
    # 画出投影图
    for j in range(h):
        for i in range(h_h[j]):
            hprojection[j,i] = 255

    cv2.imshow('hpro', hprojection)

    return h_h

# 垂直反向投影
def vProject(binary):
    h, w = binary.shape
    # 垂直投影
    vprojection = np.zeros(binary.shape, dtype=np.uint8)

    # 创建 w 长度都为0的数组
    w_w = [0]*w
    for i in range(w):
        for j in range(h):
            if binary[j, i ] == 0:
                w_w[i] += 1

    for i in range(w):
        for j in range(w_w[i]):
            vprojection[j,i] = 255

    cv2.imshow('vpro', vprojection)

    w_w_t = [item - 1 for item in w_w]

    return w_w

def vsplit(cropImg):
    w_w = vProject(cropImg)
    h, w = cropImg.shape
    position = []
    wstart , wend, w_start, w_end = 0, 0, 0, 0
    for j in range(len(w_w)):
        if w_w[j] > 0 and wstart == 0:
            w_start = j
            wstart = 1
            wend = 0
        #if w_w[j] ==0 and wstart == 1:
        if w_w[j] <= 1 and wstart == 1:
            w_end = j
            wstart = 0
            wend = 1

        if wend == 1 and w_end - w_start > 2:
            position.append([w_start, 0, w_end, h])
            wend = 0
    for p in position:
        cv2.rectangle(cropImg, (p[0], p[1]), (p[2], p[3]), (0, 0, 255), 2)

    cv2.imshow("cropImg", cropImg)

if __name__ == '__main__':
    img = cv2.imread('./tmp3.jpg')
    img = cv2.resize(img, (500, 200))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, th = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
    h,w = th.shape
    h_h = vProject(th)
    vsplit(gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

'''
def main():
    img = cv2.imread('./tmp3.jpg')
    # 可选
    #img = cv2.resize(img, (500, 200), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 针对不同图需要调整阈值
    ret, th = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
    h,w = th.shape
    h_h = hProject(th)

    start = 0
    h_start, h_end = [], []
    position = []

    # 根据水平投影获取垂直分割
    for i in range(len(h_h)):
        if h_h[i] > 0 and start == 0:
            h_start.append(i)
            start = 1
        if h_h[i] ==0 and start == 1:
            h_end.append(i)
            start = 0

    for i in range(len(h_start)):
        cropImg = th[h_start[i]:h_end[i], 0:w]
        if i ==0:
            cv2.imshow('cropimg', cropImg)
            cv2.imwrite('words_cropimg.jpg', cropImg)
        w_w = vProject(cropImg)

        wstart , wend, w_start, w_end = 0, 0, 0, 0
        for j in range(len(w_w)):
            if w_w[j] > 0 and wstart == 0:
                w_start = j
                wstart = 1
                wend = 0
            if w_w[j] ==0 and wstart == 1:
                w_end = j
                wstart = 0
                wend = 1

            # 当确认了起点和终点之后保存坐标
            if wend == 1:
                position.append([w_start, h_start[i], w_end, h_end[i]])
                wend = 0

    # 确定分割位置
    for p in position:
        cv2.rectangle(img, (p[0], p[1]), (p[2], p[3]), (0, 0, 255), 2)

    cv2.imshow('image', img)
    cv2.imwrite('vimg.jpg', img)
    cv2.imshow('th', th)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
'''
