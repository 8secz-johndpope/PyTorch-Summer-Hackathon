import os
import numpy as np
import cv2
import json
import argparse

parser = argparse.ArgumentParser(description='merge images from different videos')
parser.add_argument('--img1', default = './merge_test_imgs/003727.jpg', type=str, help='video from DB')
parser.add_argument('--img2', default = './merge_test_imgs/000489.jpg', type=str, help='video from user')
parser.add_argument('--json', default = './images_for_zh.json', type=str, help='predicted keypoints')

def ReadImg(path):
    img = cv2.imread(path)
    return img

def ReadJSON(path):
    with open(path, 'r') as f:
        all_images = json.load(f)['images']
        f.close()
        img1_keypoints = all_images[1]['003727']
        img1_bbox = all_images[1]['bounding_box']
        img2_keypoints = all_images[0]['000489']
        img2_bbox = all_images[0]['bounding_box']
        return img1_keypoints, img1_bbox, img2_keypoints, img2_bbox

def WidthHeightOfHuman(img1_bbox, img2_bbox):
    img1_w = img1_bbox[1][0] - img1_bbox[0][0]
    img1_h = img1_bbox[1][1] - img1_bbox[0][1]
    img2_w = img2_bbox[1][0] - img2_bbox[0][0]
    img2_h = img2_bbox[1][1] - img2_bbox[0][1]
    return img1_w, img1_h, img2_w, img2_h

def ResizeImg(img1, img1_bbox, img1_w, img1_h, img2_w, img2_h):
    ratio_w = img2_w / img1_w
    ratio_h = img2_h / img1_h
    H, W, _ = img1.shape
    new_W = round(W * ratio_w)
    new_H = round(H * ratio_h)
    new_img1 = cv2.resize(img1, (new_W, new_H))
    img1_bbox_pt1_x = img1_bbox[0][0]
    img1_bbox_pt1_y = img1_bbox[0][1]
    new_img1_bbox_pt1_x = round(img1_bbox_pt1_x * ratio_w)
    new_img1_bbox_pt1_y = round(img1_bbox_pt1_y * ratio_h)
    return new_img1, new_img1_bbox_pt1_x, new_img1_bbox_pt1_y

def CropImg(img1, img2, img1_bbox_pt1_x, img1_bbox_pt1_y, img2_bbox):
    img2_bbox_pt1_x = img2_bbox[0][0]
    img2_bbox_pt1_y = img2_bbox[0][1]
    H, W, _ = img2.shape
    right_margin = W - img2_bbox_pt1_x
    up_margin = H - img2_bbox_pt1_y
    img1_cropped = img1[img1_bbox_pt1_y - img2_bbox_pt1_y : img1_bbox_pt1_y + up_margin, img1_bbox_pt1_x - img2_bbox_pt1_x : img1_bbox_pt1_x + right_margin]
    return img1_cropped

def ResizeDBImg(img1, img2):
    H, W, _ = img2.shape
    new_img1 = cv2.resize(img1, (W, H))
    return new_img1

def main():
    args = parser.parse_args()
    img1 = ReadImg(args.img1)
    img2 = ReadImg(args.img2)
    img1_keypoints, img1_bbox, img2_keypoints, img2_bbox = ReadJSON(args.json)

    if img1.shape[0]*img1.shape[1] < img2.shape[0]*img2.shape[1]:
        img1_w, img1_h, img2_w, img2_h = WidthHeightOfHuman(img1_bbox, img2_bbox)
        new_img1, new_img1_bbox_pt1_x, new_img1_bbox_pt1_y = ResizeImg(img1, img1_bbox, img1_w, img1_h, img2_w, img2_h)
        img1_cropped = CropImg(new_img1, img2, new_img1_bbox_pt1_x, new_img1_bbox_pt1_y, img2_bbox)
    else:
        img1_w, img1_h, img2_w, img2_h = WidthHeightOfHuman(img2_bbox, img1_bbox)
        new_img1, new_img1_bbox_pt1_x, new_img1_bbox_pt1_y = ResizeImg(img2, img2_bbox, img1_w, img1_h, img2_w, img2_h)
        img1_cropped = CropImg(new_img1, img1, new_img1_bbox_pt1_x, new_img1_bbox_pt1_y, img1_bbox)

    # print(img1.shape)
    # print(img2.shape)
    # print(img1_w, img1_h)
    # print(img2_w, img2_h)
    # print(new_img1.shape)
    # new_img1 = ResizeDBImg(img1, img2)
    cv2.imwrite('new.jpg', new_img1)

if __name__ == '__main__':
    main()