import cv2
import matplotlib.pyplot as plt
import numpy as np
import pickle
model = pickle.load(open('data\knnpickle_file', 'rb'))

def objDect(path, number_ans):
    img = cv2.imread(path,0)
    blur = cv2.GaussianBlur(img,(5,5),0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)

    horizalLine = thresh
    verticalLine = thresh

    scale_height = 20  
    scale_long = 15

    long = int(img.shape[1]/scale_long)
    height = int(img.shape[0]/scale_height)

    horizalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (long, 1))
    horizalLine = cv2.erode(horizalLine, horizalStructure, (-1, -1))
    horizalLine = cv2.dilate(horizalLine, horizalStructure, (-1, -1))

    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, height))
    verticalLine = cv2.erode(verticalLine, verticalStructure, (-1, -1))
    verticalLine = cv2.dilate(verticalLine, verticalStructure, (-1, -1))

    mask = verticalLine + horizalLine

    contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    max = -1
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if cv2.contourArea(cnt) > max:
            x_max, y_max, w_max, h_max = x, y, w, h
            max = cv2.contourArea(cnt)

    table = img[y_max:y_max+h_max, x_max:x_max+w_max]

    cropped_thresh_img = []
    cropped_origin_img = []
    countours_img = []

    NUM_ROWS = 26
    START_ROW = 1
    for i in range(START_ROW, NUM_ROWS):
        thresh1 = thresh[y_max + round(i*h_max/NUM_ROWS)+1:y_max + round((i+1)*h_max/NUM_ROWS)-1, x_max + round(w_max/4)+5:x_max +round(w_max/2)-5]
        contours_thresh1, hierarchy_thresh1 = cv2.findContours(thresh1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        origin1 = img[y_max + round(i*h_max/NUM_ROWS)+1:y_max + round((i+1)*h_max/NUM_ROWS)-1, x_max + round(w_max/4)+5:x_max +round(w_max/2)-5]

        cropped_thresh_img.append(thresh1)
        cropped_origin_img.append(origin1)
        countours_img.append(contours_thresh1)

    for i in range(START_ROW, NUM_ROWS):
        thresh1 = thresh[y_max + round(i*h_max/NUM_ROWS)+1:y_max + round((i+1)*h_max/NUM_ROWS)-1, x_max + round(3*w_max/4)+5:x_max +round(w_max)-5]
        contours_thresh1, hierarchy_thresh1 = cv2.findContours(thresh1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        origin1 = img[y_max + round(i*h_max/NUM_ROWS)+1:y_max + round((i+1)*h_max/NUM_ROWS)-1, x_max + round(3*w_max/4)+5:x_max +round(w_max)-5]

        cropped_thresh_img.append(thresh1)
        cropped_origin_img.append(origin1)
        countours_img.append(contours_thresh1)

    answer_img = {}
    for i, countour_img in enumerate(countours_img):
        for cnt in countour_img:
            if cv2.contourArea(cnt) > 30:
                x,y,w,h = cv2.boundingRect(cnt)
                if x > cropped_origin_img[i].shape[1]*0.01 and x < cropped_origin_img[i].shape[1]*0.9:
                    answer = cropped_origin_img[i][y-2:y+h+2, x-5:x+w+5]
                    answer = cv2.threshold(answer, 160, 255, cv2.THRESH_BINARY_INV)[1]
                    answer_img[i] = answer

    kernel = np.ones((2,2), np.uint8)
    for key in answer_img.keys():
        answer_img[key] = cv2.resize(answer_img[key], (28, 28), interpolation= cv2.INTER_LINEAR)

    y_predict = {}

    for i in range(1, 50):
        y_predict[i] = 'X'

    for key in answer_img.keys():
        res = model.predict(answer_img[key].reshape(-1,784))
        if res == 3.0:
            y_predict[key] = 'D'
        elif res == 2.0:
            y_predict[key] = 'C'
        elif res == 1.0:
            y_predict[key] = 'B'
        else:
            y_predict[key] = 'A'
            
    return y_predict        


