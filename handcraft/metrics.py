from gt_visual import get_sorted_dict
from gt_visual import draw_2 as draw

import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
from box_refine import Post_Process

xml_path = '../ali_json/train/page/page'
json_path = '../train/json'
img_path = '../ali_json/train/imgs'
#img_path = '../ali_json/train/test'

def IOU(Xmlframe, Jsonframe):
    """
    自定义函数，计算两矩形 IOU，传入为均为矩形对角线，（x,y）  坐标。·
    xml 输入
    <class 'list'>: [(119, 967), (953, 967), (953, 1335), (119, 1335)]
    Json 输入
    <class 'list'>: [[{'x': 164, 'y': 67}, {'x': 896, 'y': 80}, {'x': 895, 'y': 121}, {'x': 164, 'y': 118}]]
    """

    x1 = Xmlframe[0][0];# 119
    y1 = Xmlframe[0][1];# 967
    width1 = Xmlframe[2][0] - Xmlframe[0][0];
            #Xmlframe[1][0] - Xmlframe[3][0]; xml是标准的应该问题不大
    height1 = Xmlframe[3][1] - Xmlframe[1][1];
            #Xmlframe[2][1] - Xmlframe[0][1];



    x2 = Jsonframe[0][0]
    y2 = Jsonframe[0][1]

    width2 = Jsonframe[1][0] - Jsonframe[0][0]
    height2 = Jsonframe[1][1] - Jsonframe[0][1]

    endx = max(x1 + width1, x2 + width2);
    startx = min(x1, x2);
    width = width1 + width2 - (endx - startx);

    endy = max(y1 + height1, y2 + height2);
    starty = min(y1, y2);
    height = height1 + height2 - (endy - starty);

    if width <= 0 or height <= 0:
        ratio = 0  # 重叠率为 0
    else:
        Area = width * height;  # 两矩形相交面积
        Area1 = width1 * height1;
        Area2 = width2 * height2;
        ratio = Area * 1. / (Area1 + Area2 - Area)
    # return IOU

    if width <= 0 or height <= 0:
        ratio_h = 0  # 重叠率为 0
    else:
        Area_h =  height;  # 两矩形相交面积
        Area1_h =  height1;
        Area2_h =  height2;
        ratio_h = Area_h * 1. / (Area2_h)

    return ratio

def meanIouandF1measure(imgName, template_path):

    image = cv2.imread('../ali_json/train/imgs/' + imgName)
    xmlName = imgName.split(".png")[0]+'.xml'
    jsonName = imgName.split(".png")[0]+'.json'
    xmlNamePath = os.path.join(xml_path,xmlName)
    imgNamePath = os.path.join(img_path,imgName)
    jsonNamePath = os.path.join(json_path,jsonName);

    xml_region, baseline, boxes = get_sorted_dict(xmlNamePath)
    #json_region,part = getJsonRect(jsonNamePath)
    image_f_path = img_path + '/' + imgName
    image_f = cv2.imread(image_f_path)
    post_process = Post_Process(image_f, image_f_path, template_path)
    json_region = post_process.refine_box()

    draw(xml_region, image)
    res_IOU = []
    res_F1Measure = []

    for i in range(len(json_region)):
        iou = 0
        f1_Measure = 0
        for j in range(len(xml_region)):
            iou = max(iou, IOU(xml_region[j], json_region[i]))
            image = draw_with_text(image, json_region[i], iou)
            f1_Measure = max(f1_Measure, F1Measure(xml_region[j], json_region[i]))
        res_F1Measure.append(f1_Measure)
        res_IOU.append(iou)
    print(res_IOU)
    print("  IOU平均: " + str(np.array(res_IOU).mean()))
    cv2.imwrite('./compare/' + imgName, image)
    print(res_F1Measure)
    print("  F1平均: " + str(np.array(res_F1Measure).mean()))

    res_MAPHelper = []
    precision = []

    varible = 0.1
    while(varible <= 1):
        for i in res_IOU:
            if(i > varible):
                res_MAPHelper.append(1)
            else:
                res_MAPHelper.append(0)
        tp = res_MAPHelper.count(1)
        fn = res_IOU.count(0)
        fp = res_MAPHelper.count(0) - fn
        # print(tp, fn, fp)
        precision.append(tp / (tp + fp))
        varible += 0.1
        res_MAPHelper.clear()
    res_presion = np.array(precision).mean()
    #print(res_presion)

    return np.array(res_IOU).mean(), np.array(res_F1Measure).mean(), res_IOU, res_F1Measure


def F1Measure(Xmlframe, Jsonframe):
    """
    自定义函数，计算两矩形 IOU，传入为均为矩形对角线，（x,y）  坐标。·
    xml 输入
    <class 'list'>: [(119, 967), (953, 967), (953, 1335), (119, 1335)]
    Json 输入
    <class 'list'>: [[{'x': 164, 'y': 67}, {'x': 896, 'y': 80}, {'x': 895, 'y': 121}, {'x': 164, 'y': 118}]]
    """
    x1 = Xmlframe[0][0];  # 119
    y1 = Xmlframe[0][1];  # 967
    width1 = Xmlframe[2][0] - Xmlframe[0][0];
    # Xmlframe[1][0] - Xmlframe[3][0]; xml是标准的应该问题不大
    height1 = Xmlframe[3][1] - Xmlframe[1][1];
    # Xmlframe[2][1] - Xmlframe[0][1];

    x2 = Jsonframe[0][0]
    y2 = Jsonframe[0][1]

    width2 = Jsonframe[1][0] - Jsonframe[0][0]
    height2 = Jsonframe[1][1] - Jsonframe[0][1]

    endx = max(x1 + width1, x2 + width2);
    startx = min(x1, x2);
    width = width1 + width2 - (endx - startx);

    endy = max(y1 + height1, y2 + height2);
    starty = min(y1, y2);
    height = height1 + height2 - (endy - starty);

    if width <= 0 or height <= 0:
        ratio = 0  # 重叠率为 0
        f1_Measure = 0; #TP = 0

    else:
        TP = width * height;  # 两矩形相交面积
        FN = width1 * height1 - TP;
        FP = width2 * height2 - TP;
        recall = Recall(TP, FN);
        precision = Precision(TP, FP);
        f1_Measure = Measure(precision, recall);

    if width <= 0 or height <= 0:
        ratio = 0  # 重叠率为 0
        f1_Measure_h = 0; #TP = 0

    else:
        TP_h =  height;  # 两矩形相交面积
        FN_h =  height1 - TP_h;
        FP_h =  height2 - TP_h;
        recall_h = Recall(TP_h, FN_h);
        precision_h = Precision(TP_h, FP_h);
        f1_Measure_h = Measure(precision_h, recall_h);
    # return f1_Measure
    return f1_Measure



#定义 Recall, Precision
def Recall(TP, FN):
    recall = ((TP) / (TP + FN))
    return recall

def Precision(TP, FP):
    precision = ((TP) / (TP + FP))
    return precision

#定义F1_measure
def Measure(precision, recall):
    f1measure = 2.*precision*recall / (precision + recall)
    return f1measure

def draw_with_text(img, coord, value):

    cv2.rectangle(img, coord[0], coord[1], (0,0,255), 2)
    cv2.putText(img, str(value), coord[0], cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 1)

    return img


if __name__ == '__main__':
    i = 1
    iou_all = 0
    f1_all = 0
    template_path = './numbers/'
    for filename in os.listdir(img_path):
        print(filename)
        print("第 {} 张图片数据：".format(i))
        iou, f1, iou_list, f1_list = meanIouandF1measure(filename, template_path)
        iou_all += iou
        f1_all += f1
        i += 1

    mean_iou_all = iou_all / i
    mean_f1_all = f1_all / i

    print(mean_iou_all)
    print(mean_f1_all)
    # print("ok");
    #meanIouandF1measure("0533_001.pdf_3.png")

    filename = "0533_001.pdf_5"
    #test_for_one(filename)
