import os
import cv2
import numpy as np
import itertools

class NumDetection:

    def __init__(self, image_path, template_path):
        self.image_path = image_path
        self.template_path = template_path

    def remove_repetition_locs(self, locs_list):

        for a, b in itertools.combinations(locs_list, 2):
            if a == b:
                continue
            elif abs(a[0] - b[0]) + abs(a[1] - b[1]) < 10:
                if a in locs_list:
                    locs_list.remove(a)
                else:
                    continue

        return locs_list
    def remove_far_locs(self, locs_list):
        for a, b in itertools.combinations(locs_list, 2):
            if a == b:
                continue
            elif abs(a[0] - b[0]) > 100:
                if a in locs_list:
                    locs_list.remove(a)
                else:
                    continue
        return locs_list

    def template_match(self):
        image = cv2.imread(self.image_path)
        (h_img, w_img) = image.shape[:-1]
        threshold = 0.8
        loc_list = []
        for temp in os.listdir(self.template_path):
            template = cv2.imread(self.template_path + temp)
            h, w = template.shape[0], template.shape[1]
            res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (7,249,151), 2)
                loc_list.append(pt)

        loc_list = self.remove_repetition_locs(loc_list)
        #loc_list = self.remove_far_locs(loc_list)
        loc_list.sort(key=lambda x: x[1])
        for count, item in enumerate(loc_list):
            cv2.circle(image, item, 2, [0,0,255], 2)
            cv2.line(image, item, (item[0] + w_img, item[1]), [0, 0, 255], 2)
            '''
            if count < len(loc_list) - 1:
                cv2.line(image, loc_list[count], (loc_list[count][0], loc_list[count+1][1]), [0,0,255], 2)
            else:
                cv2.line(image, loc_list[count], (loc_list[count][0], h), [0, 0, 255], 2)
            '''
        return image,loc_list


if __name__ == '__main__':
    image_path = "./test/0533_001.pdf_19.png"
    template_path = './numbers/'

    num_detection = NumDetection(image_path, template_path)

    result_img, result_locs = num_detection.template_match()

    print(len(result_locs))
    for item in result_locs:
        print(item)

    cv2.imwrite('result_locs.png', result_img)
