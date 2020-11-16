import os
import random
import numpy as np
import xml.etree.ElementTree as ET
import cv2
import matplotlib.pyplot as plt
def resolve(xml):
    tree = ET.parse(xml)
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

def draw_empty(coords, image, is_box = True, filename=False):
    img = cv2.imread(image)
    img_empty = np.zeros(img.shape, np.uint8)
    img_empty.fill(255)
    for order, item in enumerate(coords.values()):
        #cv2.putText(img_empty, str(order), item[0], cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)
        #cv2.rectangle(img, coords[0], coords[3], (255, 0, 0), 5)
        length = len(item)
        for count, point in enumerate(item):
            if count == 0:
                pass
            else:
                cv2.line(img_empty, item[count -1], item[count], (0, 255, 0), 5)
        if is_box:
            cv2.line(img_empty, item[-1], item[0], (0, 255, 0), 5)


    # cv2.imshow('img', img)
    img_empty = cv2.cvtColor(img_empty, cv2.COLOR_RGB2GRAY)
    #_, img_empty = cv2.threshold(img_empty, 200, 255, cv2.THRESH_BINARY_INV)
    _, img_empty = cv2.threshold(img_empty, 200, 255, cv2.THRESH_BINARY)
    noZero = cv2.findNonZero(img_empty)

    if filename == False:
        cv2.imwrite('tmp3.jpg', img_empty)
    else:
        cv2.imwrite(filename, img_empty)
    # cv2.waitKey(0)


def draw(coords, image, is_box = True):
    img = cv2.imread(image)
    img_empty = np.zeros(img.shape, np.uint8)
    img_empty.fill(255)
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
    cv2.imwrite('tmp3.jpg', img)
    # cv2.waitKey(0)


def get_coords(region, baseline, line):
    region_dict = {}
    boxes_dict = {}
    baseline_dict = {}
    for count, item in enumerate(region):
        region_dict[count] = item.split(' ')
    for item in region_dict:
        region_dict[item] = list(tuple(map(int, x.split(','))) for x in region_dict[item])

    for count, item in enumerate(baseline):
        baseline_dict[count] = item.split(' ')
    for item in baseline_dict:
        baseline_dict[item] = list(tuple(map(int, x.split(','))) for x in baseline_dict[item])

    for count, item in enumerate(line):
        boxes_dict[count] = item.split(' ')
    for item in baseline_dict:
        boxes_dict[item] = list(tuple(map(int, x.split(','))) for x in boxes_dict[item])

    return region_dict, baseline_dict, boxes_dict

def bound(num):

    pass

def sorting(point_dict):

    #sort_result = sorted(point_dict.items(), key = lambda kv: (kv[1][0][0], kv[1][0][1]))
    sort_result = sorted(point_dict.items(), key = lambda kv: (kv[1][0]))
    '''
    first_point_x = []
    first_point_y = []
    last_point_x = []
    for count, item in enumerate(sort_result):
        first_point_x.append(item[1][0][0])
        first_point_y.append(item[1][0][1])
        last_point_x.append(item[1][-1][0])
    '''
    updated_key_dict = {}
    for count, value in enumerate(dict(sort_result).values()):
        updated_key_dict[count] = value


    return updated_key_dict

def get_sorted_dict(xml):
    region_points, baseline_points, line_boxes = resolve(xml)
    region_dict, baseline_dict, boxes_dict = get_coords(region_points,
                                                        baseline_points,
                                                        line_boxes)

    region_dict = sorting(region_dict)
    baseline_dict = sorting(baseline_dict)
    boxes_dict = sorting(boxes_dict)

    return region_dict, baseline_dict, boxes_dict

def rough_grouping(point_dict):
    first_point = []
    for key, value in point_dict.items():
        first_point.append(value[0])

    return first_point


def all():
    save_path = './images/'
    for xml in os.listdir('./page/'):
        img = './input/' + xml.split('.')[0] + '.jpg'
        region, baseline, boxes = get_sorted_dict('./page/' + xml)
        draw_empty(baseline, img, is_box = False, filename=img)

if __name__ == '__main__':

    all()
    '''
    xml_path = '../data/example/ex2/page/38267-156938438393.xml'
    image_path = '../data/example/ex2/38267-156938438393.jpg'
    #xml_path = './page/test_Page_01.xml'
    #image_path = './input1/test_Page_01.jpg'
    region, baseline, boxes = get_sorted_dict(xml_path)
    #a = rough_grouping(baseline)
    draw_empty(baseline, image_path, is_box = False)
    #draw(baseline, image_path, is_box = False)
    '''
