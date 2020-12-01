from gt_visual import get_sorted_dict
from draw_boxes import Draw_boxes
import os
from resolve import Resolve
import cv2
import matplotlib.pyplot as plt
import numpy as np
xml_path = './train/page'
json_path = './train/json'
img_path = './train/imgs'

def getJsonRect(json_f):
    resovle_value = Resolve(json_f)
    item = resovle_value.resolve_item()
    part = resovle_value.resolve_part()
    return item, part


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


    Jsonframe = Jsonframe[0];
    x2 = min(Jsonframe[0]['x'],Jsonframe[3]['x']) #可能识别出来是4边形，往大的算成一个矩形
    y2 = min(Jsonframe[0]['y'],Jsonframe[1]['y'])

    width2 = max(Jsonframe[2]['x'] - Jsonframe[0]['x'],Jsonframe[1]['x'] - Jsonframe[3]['x']) #对角线相减
    height2 = max(Jsonframe[2]['y'] - Jsonframe[0]['y'],Jsonframe[3]['y'] - Jsonframe[1]['y'])

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
    return ratio

def meanIouandF1measure(imgName):
    xmlName = imgName.split(".png")[0]+'.xml'
    jsonName = imgName.split(".png")[0]+'.json'
    xmlNamePath = os.path.join(xml_path,xmlName)
    imgNamePath = os.path.join(img_path,imgName)
    jsonNamePath = os.path.join(json_path,jsonName);

    xml_region, baseline, boxes = get_sorted_dict(xmlNamePath)
    json_region,part = getJsonRect(jsonNamePath)


    res_IOU = []
    res_F1Measure = []

    for i in range(len(json_region)):
        iou = 0
        f1_Measure = 0
        for j in range(len(xml_region)):
            iou = max(iou, IOU(xml_region[j], json_region[i]))
            f1_Measure = max(f1_Measure, F1Measure(xml_region[j], json_region[i]))
        res_F1Measure.append(f1_Measure)
        res_IOU.append(iou)
    print(res_IOU)
    print("  IOU平均: " + str(np.array(res_IOU).mean()))
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

    return np.array(res_IOU).mean(), np.array(res_F1Measure).mean()


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

    Jsonframe = Jsonframe[0];
    x2 = min(Jsonframe[0]['x'], Jsonframe[3]['x'])  # 可能识别出来是4边形，往大的算成一个矩形
    y2 = min(Jsonframe[0]['y'], Jsonframe[1]['y'])

    width2 = max(Jsonframe[2]['x'] - Jsonframe[0]['x'], Jsonframe[1]['x'] - Jsonframe[3]['x'])  # 对角线相减
    height2 = max(Jsonframe[2]['y'] - Jsonframe[0]['y'], Jsonframe[3]['y'] - Jsonframe[1]['y'])

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



if __name__ == '__main__':
    i = 1
    iou_all = 0
    f1_all = 0
    for filename in os.listdir('./train/imgs'):
        #print(filename)
        print("第 {} 张图片数据：".format(i))
        iou, f1 = meanIouandF1measure(filename)
        iou_all += iou
        f1_all += f1
        i += 1

    print(iou_all)
    print(f1_all)
    mean_iou_all = iou_all / i
    mean_f1_all = f1_all / i

    print(mean_iou_all)
    print(mean_f1_all)
    # print("ok");
    #meanIouandF1measure("0533_001.pdf_3.png")
