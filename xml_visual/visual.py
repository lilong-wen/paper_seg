import numpy as np
import xml.etree.ElementTree as ET
import cv2
import matplotlib.pyplot as plt
def resolve(xml):
    tree = ET.parse(xml_path)
    textRegion = []
    obj_textRegion_coords = []
    val_textRegion_coords = []
    obj_textLine = []
    val_textLine_baselines = []
    val_textLine_boxes = []

    root = tree.getroot()
    #print(root.tag.split('}')[1])
    metaData = root[0]
    page = root[1]
    for region in page:
        textRegion.append(region)

    for count, region in enumerate(textRegion):
        print(f"resolve region {count}")
        tmp = []
        for item in region:
            tmp.append(item)

        obj_textRegion_coords.append(tmp[0])
        obj_textLine += tmp[1:]

    for region in obj_textRegion_coords:
        val_textRegion_coords.append(region.attrib['points'])
    for line in obj_textLine:
        val_textLine_baselines.append(line[0].attrib['points'])
        val_textLine_boxes.append(line[1].attrib['points'])

    # print(len(val_textRegion_coords))
    # print(len(val_textLine_baselines))
    # print(len(val_textLine_boxes))
    return val_textRegion_coords, val_textLine_boxes, val_textLine_baselines

def draw(coords, image, is_box = True):
    img = cv2.imread(image)
    for order, item in enumerate(coords.values()):
        cv2.putText(img, str(order), item[0], cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)
        #cv2.rectangle(img, coords[0], coords[3], (255, 0, 0), 5)
        length = len(item)
        for count, point in enumerate(item):
            if count == 0:
                pass
            else:
                cv2.line(img, item[count -1], item[count], (0, 255, 0), 5)
        if is_box:
            cv2.line(img, item[-1], item[0], (0, 255, 0), 5)


    # cv2.imshow('img', img)
    cv2.imwrite('tmp.jpg', img)
    # cv2.waitKey(0)


def get_coords(region, baseline, line):
    region_dict = {}
    boxes_dict = {}
    baseline_dict = {}
    for count, item in enumerate(region_points):
        region_dict[count] = item.split(' ')
    for item in region_dict:
        region_dict[item] = list(tuple(map(int, x.split(','))) for x in region_dict[item])

    for count, item in enumerate(baseline_points):
        baseline_dict[count] = item.split(' ')
    for item in baseline_dict:
        baseline_dict[item] = list(tuple(map(int, x.split(','))) for x in baseline_dict[item])

    for count, item in enumerate(line_boxes):
        boxes_dict[count] = item.split(' ')
    for item in baseline_dict:
        boxes_dict[item] = list(tuple(map(int, x.split(','))) for x in boxes_dict[item])

    return region_dict, baseline_dict, boxes_dict

def column_grouping(baseline):

    sort_result = sorted(baseline.items(), key = lambda kv: kv[1][0])
    first_point_x = []
    first_point_y = []
    last_point_x = []
    for count, item in enumerate(sort_result):
        first_point_x.append(item[1][0][0])
        first_point_y.append(item[1][0][1])
        last_point_x.append(item[1][-1][0])


    return dict(sort_result)


if __name__ == '__main__':
    xml_path = './page/38267-156938438393.xml'
    image_path = './38267-156938438393.jpg'
    region_points, baseline_points, line_boxes = resolve(xml_path)
    region_dict, baseline_dict, boxes_dict = get_coords(region_points,
                                                        baseline_points,
                                                        line_boxes)

    #draw(baseline_dict, image_path, is_box = False)
    #draw(region_dict, image_path, is_box = False)
    a = column_grouping(baseline_dict)
    draw(a, image_path, is_box = False)
