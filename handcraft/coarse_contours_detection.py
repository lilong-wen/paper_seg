import cv2
import itertools

class Find_Max_Contours:

    def __init__(self, image):

        self.img = image

    def remove_small_boxes(self, coords):

        for a, b in itertools.combinations(coords, 2 ):
            if a[0] > b[0] and a[0] < b[0] + b[2]:
                if a in coords:
                    coords.remove(a)
        return coords

    def find_contours(self):

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7,7), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Create rectangular structuring element and dilate
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        dilate = cv2.dilate(thresh, kernel, iterations=10)

        # Find contours and draw rectangle
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        coords_list = []
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            coords_list.append((x,y,w,h))
            #cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)

        coords = self.remove_small_boxes(coords_list)
        for item in coords:
            (x,y,w,h) = item
            cv2.rectangle(self.img, (x, y), (x + w, y + h), (0,0,255), 2)
        return self.img, coords


if __name__ == '__main__':

    image = cv2.imread("./test.png")

    find_max_contours = Find_Max_Contours(image)
    result_img, _ = find_max_contours.find_contours()
    cv2.imwrite("contours.png", result_img)
