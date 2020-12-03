import cv2

from coarse_contours_detection import Find_Max_Contours
from num_detection import NumDetection

def draw_box_line(line_coords, box_coords, image):

    (h_img, w_img) = image.shape[:-1]
    for item in box_coords:
        (x,y,w,h) = item
        cv2.rectangle(image, (x, y), (x + w, y + h), (0,0,255), 2)

    for count, item in enumerate(line_coords):
        cv2.circle(image, item, 2, [0,0,255], 2)
        if item[0] > x:
            x1 = x
            y1 = item[1]
        if item[0] + w_img > x + w:
            x2 = x + w
            y2 = item[1]

        #cv2.line(image, item, (item[0] + w_img, item[1]), [0, 0, 255], 2)
        cv2.line(image, (x1, y1), (x2, y2), [0, 0, 255], 2)


    return image

if __name__ == '__main__':

    image_path = './test/0533_001.pdf_18.png'
    template_path = './numbers/'

    origin_img = cv2.imread(image_path)

    num_detection = NumDetection(image_path, template_path)

    result_img, result_locs = num_detection.template_match()

    find_max_contours = Find_Max_Contours(origin_img)
    _, box_coords = find_max_contours.find_contours()

    img = draw_box_line(result_locs, box_coords, origin_img)

    cv2.imwrite("final_v2.png", img)
