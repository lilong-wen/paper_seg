import os
import cv2
import numpy as np


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
    ####
    for count, item in enumerate(w_w):
        if count < 3:
            continue
        elif w_w[count] != 0 and w_w[count-1] == 0 and w_w[count+1] == 0:
            w_w[count] = 0
    ###
    h, w = cropImg.shape
    position = []
    wstart , wend, w_start, w_end = 0, 0, 0, 0
    for j in range(len(w_w)):
        if w_w[j] > 0 and wstart == 0:
            w_start = j
            wstart = 1
            wend = 0
        #if w_w[j] ==0 and wstart == 1:
        if w_w[j] <= 2 and wstart == 1:
            w_end = j
            wstart = 0
            wend = 1

        if wend == 1 and w_end - w_start > int(w/100):
            position.append([w_start, 0, w_end, h])
            wend = 0
    for p in position:
        cv2.rectangle(cropImg, (p[0], p[1]), (p[2], p[3]), (0, 0, 255), 2)

    #cv2.imshow("cropImg", cropImg)
    #print(len(position))

    return cropImg, len(position)

def vsplit_process(img, name, save_path):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
    result_img, num = vsplit(gray)
    real_num = name.split('_')[0]
    print("real_num: " + str(real_num))
    print("num: " + str(num))

    cv2.imwrite(save_path + name, result_img)

    return 1 if int(real_num) == int(num) else 0


if __name__ == '__main__':
    #img = cv2.imread('./tmp3.jpg')
    #img = cv2.resize(img, (500, 200))
    #img_path = './images/'
    #save_path = './result_imgs/'
    img_path = './test/'
    save_path = './test_result/'

    count = 0
    for item in os.listdir(img_path):
        img = cv2.imread(img_path + item)
        img = cv2.resize(img, (500, 300))
        result = vsplit_process(img, item, save_path)
        count += result
        print(count)


    cv2.waitKey(0)
    cv2.destroyAllWindows()
