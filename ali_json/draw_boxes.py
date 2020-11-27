import cv2
from resolve import Resolve

class Draw_boxes:

    def __init__(self, img, json_f):
        self.img = img
        self.json_f = json_f

    def get_list(self):

        resovle_value = Resolve(self.json_f)
        item = resovle_value.resolve_item()
        part = resovle_value.resolve_part()

        return item, part


    def draw_item_part(self, part_draw=True):
        item, part = self.get_list()

        result = self.img

        for count1 in item:
            for i in count1:
                result = cv2.rectangle(result,
                                       (i[0]['x'], i[0]['y']),
                                       (i[2]['x'], i[2]['y']),
                                       (0, 0, 255),
                                       2)
        if part_draw == True:
            for count2 in part:
                for i in count2:
                    result = cv2.rectangle(result,
                                           (i[0]['x'], i[0]['y']),
                                           (i[2]['x'], i[2]['y']),
                                           (255, 0, 0),
                                           3)
        else:
            pass

        return result

if __name__ == '__main__':

    img = cv2.imread('./train/test/0533_001.pdf_2.png')
    #file_path = './json_sample.json'
    file_path = './train/json/0533_001.pdf_2.json'

    draw_boxes = Draw_boxes(img, file_path)

    result_img = draw_boxes.draw_item_part()

    cv2.imwrite('result.jpg', result_img)
