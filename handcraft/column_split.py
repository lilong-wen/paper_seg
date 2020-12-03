import os
import cv2
import numpy as np

class column_split:

    def __init__(self, image, origin):
        self.image = image
        self.origin_image = origin

    def crop_bottom(self):

        h, w, _ = self.image.shape

        crop_level_top = int(h/3)
        crop_level_bottom = int(h/3)
        cropImg = self.image[crop_level_top:-crop_level_bottom,:]

        #cv2.imshow('cop', cropImg)
        #return cropImg
        return cropImg

    def vsplit_process(self):

        crop = self.crop_bottom()
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        result_img, result_list = self.vsplit(gray, gray_crop, self.origin_image)

        return result_img, result_list

    def vsplit(self, Img, crop, origin):

        #w_w = vProject(Img)
        w_w = self.vProject(crop)
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
            cv2.rectangle(origin, (p[0], p[1]), (p[2], p[3]), (0, 0, 255), 2)

        result_list = []
        for p in position:
            result_list.append(origin[p[1]:p[3], p[0]:p[2]])

        #cv2.imshow("Img", Img)
        #print(len(position))

        #print(position)
        #print(len(position))
        #position = self.post_process(position)
        #print(position)
        #print(len(position))

        return origin, result_list


    def vProject(self, binary):
        h, w = binary.shape
        # 垂直投影
        vprojection = np.zeros(binary.shape, dtype=np.uint8)

        # 创建 w 长度都为0的数组
        w_w = [0]*w
        for i in range(w):
            for j in range(h):
                if binary[j, i ] == 0:
                    w_w[i] += 1

        w_w = self.smooth(w_w)
        for i in range(w):
            for j in range(w_w[i]):
                vprojection[j,i] = 255

        #cv2.imshow('vpro', vprojection)

        w_w_t = [item - 1 for item in w_w]

        return w_w

    def smooth(self, w):
        new_w = []
        for item in w:
            if item == 1:
                item += 33
            elif item != 0:
                item += 33
            new_w.append(item)

        return w

    def post_process_wider(self, position):

        if len(position = 2):
            position[0][0] -= int(position[0][0]/10)
            midle = int((position[0][2] + position[1][0]) / 2)

    def post_process(self, position):
        position_new = []
        max_len = 0
        num = 0

        if len(position) % 2 != 0 and len(position) != 1:
            for count, item in enumerate(position):
                if item[2] - item[0] > max_len:
                    num = count
                    max_len = item[2] - item[0]
            for count, item in enumerate(position):
                if count == num:
                    position_new.append([item[0], item[1], int(item[2]/2), item[3]])
                    position_new.append([int(item[2]/2), item[1], item[2], item[3]])
                else:
                    position_new.append(item)
        else:
            return position

        return position_new

'''
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
'''
if __name__ == '__main__':
    img = cv2.imread('./5_lines.jpg')
    origin_img = cv2.imread('./5.jpg')

    split = column_split(img, origin_img)

    result_img, result_list = split.vsplit_process()

    for count, item in enumerate(result_list):
        cv2.imwrite(str(count) + '.jpg', item)

    cv2.imwrite("result.jpg", result_img)
