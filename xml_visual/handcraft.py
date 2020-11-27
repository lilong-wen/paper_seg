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

    w_w = smooth(w_w)
    for i in range(w):
        for j in range(w_w[i]):
            vprojection[j,i] = 255

    #cv2.imshow('vpro', vprojection)

    w_w_t = [item - 1 for item in w_w]

    return w_w

def smooth(w):
    new_w = []
    for item in w:
        if item == 1:
            item += 33
        elif item != 0:
            item += 33
        new_w.append(item)

    return w

def vsplit(Img, crop):
    #w_w = vProject(Img)
    w_w = vProject(crop)
    median = np.median(w_w)
    thresh = int(median/5)

    ####
    #w_w = smooth(w_w)
    ###
    h, w = Img.shape
    position = []
    wstart , wend, w_start, w_end = 0, 0, 0, 0
    for j in range(len(w_w)):
        if w_w[j] > 0 and wstart == 0:
            w_start = j
            wstart = 1
            wend = 0

        #if w_w[j] ==0 and wstart == 1:
        # using 2 get 86%
        if w_w[j] <= thresh and wstart == 1:
            w_end = j
            wstart = 0
            wend = 1

        if wend == 1 and w_end - w_start > int(w/10):
            position.append([w_start, 0, w_end, h])
            wend = 0
    for p in position:
        cv2.rectangle(Img, (p[0], p[1]), (p[2], p[3]), (0, 0, 255), 2)

    #cv2.imshow("Img", Img)
    #print(len(position))

    return Img, len(position)

def vsplit_process(img, crop, name, save_path):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    result_img, num = vsplit(gray, gray_crop)
    real_num = name.split('_')[0]
    print("real_num: " + str(real_num))
    print("num: " + str(num))

    cv2.imwrite(save_path + name, result_img)
    #cv2.imshow('result', result_img)

    return 1 if int(real_num) == int(num) else 0

def crop_bottom(img):

    h, w, _ = img.shape

    crop_level_top = int(h/3)
    crop_level_bottom = int(h/3)
    cropImg = img[crop_level_top:-crop_level_bottom,:]

    #cv2.imshow('cop', cropImg)
    #return cropImg
    return cropImg

if __name__ == '__main__':
    #img = cv2.imread('./tmp3.jpg')
    #img = cv2.resize(img, (500, 200))
    img_path = './images/'
    save_path = './result_imgs/'
    #img_path = './test/'
    #save_path = './test_result/'

    count = 0
    for item in os.listdir(img_path):
        img = cv2.imread(img_path + item)
        h, w, _ = img.shape
        img_crop = crop_bottom(img)
        #img = cv2.resize(img, (500, 300))
        #img = cv2.resize(img, (int(h/10), int(w/10)))
        result = vsplit_process(img, img_crop, item, save_path)
        count += result
        print(count)


    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
