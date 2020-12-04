import cv2
import random

from coarse_contours_detection import Find_Max_Contours
from num_detection import NumDetection

class Post_Process:

    def __init__(self, img, image_path, template_path):

        self.img = img

        self.template_path = template_path
        self.image_path = image_path

    def assemble(self, line_coords, box_coords):

        item_split_list = []

        for item in box_coords:
            (x_box, y_box, w_box, h_box) = item

        for count, item in enumerate(line_coords):
            y_line = line_coords[count][1]
            if count < len(line_coords) - 1:
                y_line_next = line_coords[count + 1][1]
            else:
                y_line_next = h_box
            item_split_list.append(((x_box, y_line), (x_box + w_box, y_line_next)))

        return item_split_list

    def crop_img(self, loc_list):

        cropped_imgs = []
        for item in loc_list:
            cropped_imgs.append(self.img[item[0][1]:item[1][1], item[0][0]:item[1][0]])

        return cropped_imgs

    def refine_box(self):

        origin_img = self.img

        num_detection = NumDetection(self.image_path, self.template_path)
        _, result_locs = num_detection.template_match()

        find_max_contours = Find_Max_Contours(origin_img)
        _, box_coords = find_max_contours.find_contours()

        #img = draw_box_line(result_locs, box_coords, origin_img)
        #cv2.imwrite("final_tmp.png", img)

        loc_list = self.assemble(result_locs, box_coords)

        cropped_img = self.crop_img(loc_list)
        cropped_list = []
        useless_count = []
        for count, cropped_item in enumerate(cropped_img):
            #cv2.imwrite('./croped_item/' + str(count) + '.jpg', cropped_item)
            if cropped_item.shape [0] < 7 :
                useless_count.append (count)
                continue
            print (cropped_item.shape)
            find_max_contours = Find_Max_Contours(cropped_item)
            box_coords = find_max_contours.combinations_separated_parts()
            cropped_list.append(box_coords)

        for index in sorted (useless_count, reverse=True):
            del loc_list [index]
        loc_list_new = []

        for count in range(0, len(cropped_list)):
            new_1_x = loc_list[count][0][0] + cropped_list[count][0][0]
            new_1_y = loc_list[count][0][1] + cropped_list[count][0][1]

            new_2_x = loc_list[count][0][0] + cropped_list[count][1][0]
            new_2_y = loc_list[count][0][1] + cropped_list[count][1][1]

            loc_list_new.append(((new_1_x, new_1_y), (new_2_x, new_2_y)))

        '''
        for item in loc_list_new:
             B = random.randint(0, 255)
             G = random.randint(0, 255)
             R = random.randint(0, 255)
             cv2.rectangle(origin_img, item[0], item[1], [B, G, R], 2)

        cv2.imwrite('final_v3.png', origin_img)
        '''
        return loc_list_new

if __name__ == '__main__':

    #image_path = '../ali_json/train/imgs/0562_001.pdf_7.png'
    image_path = './test/0533_001.pdf_5.png'
    template_path = './numbers/'

    image = cv2.imread(image_path)
    #def __init__(self, img, line_coords, box_coords, image_path, template_path):
    post_process = Post_Process(image, image_path, template_path)
    loc_list_new = post_process.refine_box()

    for item in loc_list_new:
         B = random.randint(0, 255)
         G = random.randint(0, 255)
         R = random.randint(0, 255)
         cv2.rectangle(image, item[0], item[1], [B, G, R], 2)


    cv2.imwrite('final_v4.png', image)
