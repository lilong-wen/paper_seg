import cv2
import random

from coarse_contours_detection import Find_Max_Contours
from num_detection import NumDetection

class Post_Process:

    def __init__(self, line_coords, box_coords):

        self.line_coords = line_coords
        self.box_coords = box_coords

    def assemble(self):

        item_split_list = []

        for item in self.box_coords:
            (x_box, y_box, w_box, h_box) = item

        for count, item in enumerate(self.line_coords):
            y_line = self.line_coords[count][1]
            if count < len(self.line_coords) - 1:
                y_line_next = self.line_coords[count + 1][1]
            else:
                y_line_next = h_box
            item_split_list.append(((x_box, y_line), (x_box + w_box, y_line_next)))

        return item_split_list

def crop_img(img, loc_list):
    cropped_imgs = []
    for item in loc_list:
        cropped_imgs.append(img[item[0][1]:item[1][1], item[0][0]:item[1][0]])

    return cropped_imgs

if __name__ == '__main__':

    image_path = './test/0533_001.pdf_18.png'
    template_path = './numbers/'

    origin_img = cv2.imread(image_path)

    num_detection = NumDetection(image_path, template_path)
    _, result_locs = num_detection.template_match()

    find_max_contours = Find_Max_Contours(origin_img)
    _, box_coords = find_max_contours.find_contours()

    #img = draw_box_line(result_locs, box_coords, origin_img)
    #cv2.imwrite("final_v2.png", img)

    post_process = Post_Process(result_locs, box_coords)
    loc_list = post_process.assemble()

    cropped_img = crop_img(origin_img, loc_list)

    cropped_list = []
    for count, cropped_item in enumerate(cropped_img):
        cv2.imwrite('./croped_item/' + str(count) + '.jpg', cropped_item)
        find_max_contours = Find_Max_Contours(cropped_item)
        box_coords = find_max_contours.combinations_separated_parts()
        cropped_list.append(box_coords)


    loc_list_new = []

    for count in range(0, len(cropped_list)):
        new_1_x = loc_list[count][0][0] + cropped_list[count][0][0]
        new_1_y = loc_list[count][0][1] + cropped_list[count][0][1]

        new_2_x = loc_list[count][0][0] + cropped_list[count][1][0]
        new_2_y = loc_list[count][0][1] + cropped_list[count][1][1]

        loc_list_new.append(((new_1_x, new_1_y), (new_2_x, new_2_y)))

    for item in loc_list_new:
         B = random.randint(0, 255)
         G = random.randint(0, 255)
         R = random.randint(0, 255)
         cv2.rectangle(origin_img, item[0], item[1], [B, G, R], 2)

    cv2.imwrite('final_v3.png', origin_img)
