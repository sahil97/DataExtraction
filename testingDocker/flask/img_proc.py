#!/usr/bin/env python
# coding: utf-8

# In[80]:


# import the necessary packages
import cv2
import numpy as np
import os
import argparse
import imutils
from PIL import Image 
from pdf2image import convert_from_path


# In[99]:


def convert_to_imgs(pdfPath):
    image_list = []
    pages = convert_from_path(pdfPath, 500)
    for index in range(len(pages)):
        image_list.append(str(index)+'_out.jpg')
        pages[index].save(str(index)+'_out.jpg', 'JPEG')
    return image_list


# In[116]:


def extract_cords_from_pdf(pdfPath):
    image_list = convert_to_imgs(pdfPath)
    cords = []
    for image in image_list:
        extracted_cords = extract_cords(image)
        cords.append(extracted_cords[1])
    return cords


# In[111]:


def extract_cords(imgPath):
    cords_array = []
    # Read the image
    img = cv2.imread(imgPath, 0)

    # Thresholding the image
    (thresh, img_bin) = cv2.threshold(img, 128, 255,cv2.THRESH_BINARY|     cv2.THRESH_OTSU)
    # Invert the image
    img_bin = 255-img_bin 
    cv2.imwrite("Image_bin.jpg",img_bin)
    # Defining a kernel length
    kernel_length = np.array(img).shape[1]//80

    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # Morphological operation to detect vertical lines from an image
    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
#     cv2.imwrite("verticle_lines.jpg",verticle_lines_img)
    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
#     cv2.imwrite("horizontal_lines.jpg",horizontal_lines_img)
    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha
    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#     cv2.imwrite("img_final_bin.jpg",img_final_bin)
    # Find contours for image, which will detect all the boxes
    im2, contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Sort all the contours by top to bottom.
    (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")
    idx = 0
    for c in contours:
        # Returns the location and width,height for every contour
        x, y, w, h = cv2.boundingRect(c)
    #     print(x, y, w, h)
        if (w > 1000 and h > 800):
            idx += 1
#             HardCoding for testing, will remove later
            cords_array.append(((y+150)/5, (x-70)/7, (y+h)/7, (x+w+100)/7))
#             new_img = img[y:y+h, x:x+w]
    #         print(new_img)
    #         cv2.imwrite(os.path.join("cropped/",str(idx)) + '.png', new_img)
    #         PILimage = Image.fromarray(new_img)
    #         PILimage.save(os.path.join("cropped/",str(idx)) + '.png', dpi=(200,200))
    # # If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
        if (w > 800 and h > 500) and w>3*h:
            idx += 1
            new_img = img[y:y+h, x:x+w]
#             cv2.imwrite(os.path.join("cropped/",str(idx)) + '.png', new_img)
            PILimage = Image.fromarray(new_img)
            PILimage.save(os.path.join("cropped/",str(idx)) + '.png', dpi=(200,200))
    
    return cords_array


# In[112]:


def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0

    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
        key=lambda b:b[1][i], reverse=reverse))

    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)

