import cv2
import time
import argparse
import os
import torch
import json
import sys
from scipy import spatial
import numpy as np
import operator

import posenet
import posenet.utils as pu


# parser = argparse.ArgumentParser()
# parser.add_argument('--model', type=int, default=101)
# parser.add_argument('--scale_factor', type=float, default=1.0)
# parser.add_argument('--notxt', action='store_true')
# parser.add_argument('--image_dir', type=str, default='./posenet-pytorch/images')
# parser.add_argument('--output_dir', type=str, default='./posenet-pytorch/output')
# args = parser.parse_args()


def main():
    model = posenet.load_model(101)
    model = model.cuda()
    output_stride = model.output_stride

    # read database 
    database_path = '/home/hteam/Documents/han/PyTorch-Summer-Hackathon/backend/posenet-pytorch/4database.json'
    database = ReadJSON(database_path)
    del database['sample5']
    del database['sample3']
    del database['sample9']
    del database['sample6']
    del database['sample7']
    del database['sample8']
    del database['sample2']
    del database['sample10']
    del database['sample11']
    del database['sample12']
    del database['video_1']
    del database['video_2']
    del database['video_3']

    # if args.output_dir:
    #     if not os.path.exists(args.output_dir):
    #         os.makedirs(args.output_dir)

    # filenames = [
    #     f.path for f in sorted(os.scandir(args.image_dir), key=lambda x: (x.is_dir(), x.name)) if f.is_file() and f.path.endswith(('.png', '.jpg'))]
    image_files = video2frame(sys.argv[1])
    # image_files = video2frame('/home/hteam/Documents/han/hackathon/posenet-pytorch/videos/test_1.mp4')

    # # 輸出
    # export_filename = sys.argv[1].split('/')[-1]
    # h, w, _ = image_files[0].shape
    # os.makedirs(sys.argv[2], exist_ok=True)
    # export_path = sys.argv[2] + export_filename
    # fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    # out = cv2.VideoWriter(export_path, fourcc, 30.0, (w, h))

    count = 0  #計算frame, 10個一組
    # keypoints_list_all = []  #所有frame
    keypoints_list = {} #單一frame的所有keypoints

    frame_no = 0
    similarities_list = []
    s_frame = []
    user_frame = []

    start = time.time()
    for img in image_files:
        if count%1 != 0 or frame_no < 30*5 or frame_no >30*25:
            print(frame_no)
            frame_no += 1
            continue
    # for f in filenames:
        # out.write(img)
        # cv2.imshow('demo', img)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        input_image, draw_image, output_scale = pu._process_input(
            img, scale_factor=1.0, output_stride=output_stride)

        with torch.no_grad():
            input_image = torch.Tensor(input_image).cuda()

            heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = model(input_image)

            pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multiple_poses(
                heatmaps_result.squeeze(0),
                offsets_result.squeeze(0),
                displacement_fwd_result.squeeze(0),
                displacement_bwd_result.squeeze(0),
                output_stride=output_stride,
                max_pose_detections=10,
                min_pose_score=0.25)

        keypoint_coords *= output_scale

        
        p1 = None
        p2 = None
        area = 0
        # if not args.notxt:
        # if True:
        if count%1 == 0 and frame_no > 30*5 and frame_no <30*25:
            # print()
            # print("Results for image: %s" % f)
            for pi in range(len(pose_scores)):
                if pose_scores[pi] == 0.:
                    break

                index = 0
                max_x = 0
                max_y = 0
                min_x = 9999
                min_y = 9999
                temp_keypoints = dict()
                
                keypoints = []
                # print('Pose #%d, score = %f' % (pi, pose_scores[pi]))
                for ki, (s, c) in enumerate(zip(keypoint_scores[pi, :], keypoint_coords[pi, :, :])):
                    # print('Keypoint %s, score = %f, coord = %s' % (posenet.PART_NAMES[ki], s, c))

                    if(index > 4):  #跳過眼睛
                        keypoints.append(c.tolist())
                    else:
                        index += 1
                    if c[0] > max_x:
                        max_x = c[0]
                    if c[1] > max_y:
                        max_y = c[1]
                    if c[0] < min_x:
                        min_x = c[0]
                    if c[1] < min_y:
                        min_y = c[1]
                    
                if area < (max_x-min_x) * (max_y-min_y):
                    area = (max_x-min_x) * (max_y-min_y)
                    # keypoints_list[f[-10:-4]] = keypoints
                    # keypoints_list['test'] = keypoints
                    keypoints_list[str(frame_no)] = keypoints
                    p1 = (int(min_y),int(min_x))
                    p2 = (int(max_y),int(max_x))
        
        # if count%10 == 0 and frame_no > 30*5 and frame_no <30*25:
        # # if True:
            # for key in keypoints_list.keys():
            if str(frame_no) in keypoints_list:
                key, similarity = vote(keypoints_list[str(frame_no)], database)
                s_frame.append(key)
                similarities_list.append(similarity)
                user_frame.append(frame_no)
                
            # keypoints_list_all.append(keypoints_list)
            # keypoints_list = {}

        print(frame_no)
        frame_no += 1
        count += 1

        # if args.output_dir:
        #     draw_image = posenet.draw_skel_and_kp(
        #         draw_image, pose_scores, keypoint_scores, keypoint_coords,
        #         min_pose_score=0.25, min_part_score=0.25)
        #     if p1 != None and p2 != None:
        #         # cv
        #         pass    return video_save_path
        #     cv2.imwrite(os.path.join(args.output_dir, os.path.relpath(f, args.image_dir)), draw_image)

    # print('Average FPS:', len(image_files) / (time.time() - start))
    # print(max(similarities_list))
    # print(s_frame[similarities_list.index(max(similarities_list))])
    # print(user_frame[similarities_list.index(max(similarities_list))])
    # cv2.imshow('demo', image_files[user_frame[similarities_list.index(max(similarities_list))]])
    # cv2.waitKey(0)2.imshow('demo',img1_cropped)
    # cv2.destroyAll2.imshow('demo',img1_cropped)
    

    if len(similarities_list) == 0:
        make_video_for_no_keypoints(image_files)
    else:
        make_video(user_frame[similarities_list.index(max(similarities_list))], s_frame[similarities_list.index(max(similarities_list))], image_files, database, keypoints_list)

    # result = dict()
    # result[args.image_dir.split('/')[-2]] = keypoints_list_all
    # ret = json.dumps(result)
    # with open(args.image_dir.split('/')[-2]+'.json', 'w') as fp:
    #     fp.write(ret)
    
    
    # out.release()
    # for weiting's return
    # print('weitingsplitme' + export_filename)

def ResizeDBImg(img1, img2):
    H, W, _ = img2.shape
    new_img1 = cv2.resize(img1, (W, H))
    return new_img1

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
    img2_bbox_pt1_x = int(img2_bbox[0][0])
    img2_bbox_pt1_y = int(img2_bbox[0][1])
    H, W, _ = img2.shape
    right_margin = W - img2_bbox_pt1_x
    up_margin = H - img2_bbox_pt1_y

    # print('hihihi')
    # print(img2_bbox_pt1_x, img2_bbox_pt1_y)
    # print(H, W)
    # print(right_margin)
    # print(up_margin)
    # print('img1_bbox_pt1_y - img2_bbox_pt1_y', img1_bbox_pt1_y - img2_bbox_pt1_y)
    # print('img1_bbox_pt1_y + up_margin', img1_bbox_pt1_y + up_margin)
    # exit()

    img1_cropped = img1[img1_bbox_pt1_y - img2_bbox_pt1_y : img1_bbox_pt1_y + up_margin, img1_bbox_pt1_x - img2_bbox_pt1_x : img1_bbox_pt1_x + right_margin]
    return img1_cropped

def make_video_for_no_keypoints(image_files):
    # 輸出
    export_filename = sys.argv[1].split('/')[-1]
    os.makedirs(sys.argv[2], exist_ok=True)
    export_path = sys.argv[2] + export_filename
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')

    h, w, _ = image_files[0].shape
    out = cv2.VideoWriter(export_path, fourcc, 30.0, (w, h))
    
    for img in image_files:
        out.write(img)

    out.release()
    print('Succeed to output video.')

    # for weiting's return
    print('weitingsplitme' + export_filename)


def make_video(user_frame, database_frame, image_files, database, keypoints_list):
    # 輸出
    export_filename = sys.argv[1].split('/')[-1]
    os.makedirs(sys.argv[2], exist_ok=True)
    export_path = sys.argv[2] + export_filename
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')

    h, w, _ = image_files[0].shape
    out = cv2.VideoWriter(export_path, fourcc, 30.0, (w, h))

    for i in range(user_frame + 1):
        out.write(image_files[i])

    last_frame_from_user_video = image_files[user_frame]
    keypoints_of_last_frame_from_user_video = keypoints_list[str(user_frame)]
    bbox_of_last_frame_from_user_video = get_boundingbox(keypoints_of_last_frame_from_user_video)
    
    video_name = database_frame.split('_')[0]
    video_start_frame_number = int(database_frame.split('_')[1])
    path = '/home/hteam/Documents/han/PyTorch-Summer-Hackathon/backend/posenet-pytorch/images/' + video_name + '/'
    
    filenames = [
        f.path for f in sorted(os.scandir(path), key=lambda x: (x.is_dir(), x.name)) if f.is_file() and f.path.endswith(('.png', '.jpg'))]

    DB_first_frame = cv2.imread(filenames[0])
    DB_first_frame_keypoints = database[video_name][filenames[0].split('/')[-1][:-4]]
    DB_first_frame_bbox = get_boundingbox(DB_first_frame_keypoints)

    # user_val = cv2.rectangle(last_frame_from_user_video, (bbox_of_last_frame_from_user_video[0][0], bbox_of_last_frame_from_user_video[0][1]), (bbox_of_last_frame_from_user_video[1][0], bbox_of_last_frame_from_user_video[1][1]), (0, 255, 0), 2)
    # DB_val = cv2.rectangle(DB_first_frame, (DB_first_frame_bbox[0][0], DB_first_frame_bbox[0][1]), (DB_first_frame_bbox[1][0], DB_first_frame_bbox[1][1]), (0, 255, 0), 2)
    # cv2.imwrite('user.jpg', user_val)
    # cv2.imwrite('DB_val.jpg', DB_val)
    # print('user', bbox_of_last_frame_from_user_video)
    # print('DB', DB_first_frame_bbox)
    # exit()

    # assume 1小2大
    img1_w, img1_h, img2_w, img2_h = WidthHeightOfHuman(DB_first_frame_bbox, bbox_of_last_frame_from_user_video)
    
    
    for i in range(video_start_frame_number, len(filenames)):
        # new_img1, new_img1_bbox_pt1_x, new_img1_bbox_pt1_y = ResizeImg(cv2.imread(filenames[i]), DB_first_frame_bbox, img1_w, img1_h, img2_w, img2_h)
        # # print('new_img1', new_img1.shape)
        # # cv2.imwrite('new_img1.jpg', new_img1)
        # # exit()
        # img1_cropped = CropImg(new_img1, last_frame_from_user_video, new_img1_bbox_pt1_x, new_img1_bbox_pt1_y, bbox_of_last_frame_from_user_video)
        # # print('img1_cropped.shape', img1_cropped.shape)
        
        # # exit()
        # # cv2.imshow('demo',img1_cropped)
        # # cv2.waitKey(0)
        # # cv2.destroyAllWindows()
        # # exit(-1)
        # img1_cropped = cv2.resize(img1_cropped, (w, h))
        # out.write(img1_cropped)

        newImg = ResizeDBImg(cv2.imread(filenames[i]), last_frame_from_user_video)
        out.write(newImg)

    out.release()
    print('Succeed to output video.')

    # for weiting's return
    print('weitingsplitme' + export_filename)


def video2frame(filename):
    video = []
    vidcap = cv2.VideoCapture(filename)
    # print(filename)
    while True:
        ret, frame = vidcap.read()
        if ret:
            # cv2.imwrite(args.frames + "/%s.jpg" % str(count).zfill(6), image)     # save frame as JPEG file    
            video.append(frame)
        else:
            break

    return video

def calculate_similarity(data, input):
    data_bounding_box = get_boundingbox(data)
    input_bounding_box = get_boundingbox(input)
    data, input = scale(data, data_bounding_box, input, input_bounding_box)
    data = np.array(data).flatten()
    input = np.array(input).flatten()
    similarity = 1-spatial.distance.cosine(data, input)
    return similarity
    

def scale(data, data_bounding_box, input, input_bounding_box):
    data_y_scale = data_bounding_box[0][0]-data_bounding_box[1][0]
    input_y_scale = input_bounding_box[0][0]-input_bounding_box[1][0]

    if data_y_scale > input_y_scale:
        scale = data_y_scale/input_y_scale
        data = normalized_keypoints(data, data_bounding_box[0][0], data_bounding_box[1][0])
        input = normalized_keypoints(input, input_bounding_box[0][0], input_bounding_box[1][0],scale)
    else:
        scale = input_y_scale/data_y_scale
        data = normalized_keypoints(data, data_bounding_box[0][0], data_bounding_box[1][0],scale)
        input = normalized_keypoints(input, input_bounding_box[0][0], input_bounding_box[1][0])

    return data, input

def normalized_keypoints(data, min_x, min_y, scale=1):
    normalized_data = []
    for d in data:
        normalized_data.append([(d[0]-min_x)*scale,(d[1]-min_y)*scale])
    return normalized_data

def get_boundingbox(data):
    max_x = 0
    max_y = 0
    min_x = 9999
    min_y = 9999
    for d in data:
        # print(d)
        if int(d[0]) > max_x:
            max_x = int(d[0])
        if int(d[1]) > max_y:
            max_y = int(d[1])
        if int(d[0]) < min_x:
            min_x = int(d[0])
        if int(d[1]) < min_y:
            min_y = int(d[1])
    bounding_box = []
    bounding_box.append((min_y, min_x))
    bounding_box.append((max_y, max_x))
    return bounding_box
 

def vote(input, database):
    
    similarities = dict()
    for key in database.keys():
        index = 0
        while True:
            k = str(index).zfill(6)
            if k in database[key]:
                similarity = calculate_similarity(database[key][k], input)
                similarities[str(key)+'_'+k] = similarity
            else:
                break   
            index += 1
    max_key = max(similarities.items(), key=operator.itemgetter(1))[0]

    return max_key, similarities[max_key]

def ReadJSON(path):
    with open(path, 'r') as f:
        DB_videos = json.load(f)
        f.close()
    return DB_videos
    

# def example(data, input_units):
#     for d in range(len(data)):
#         for key in input_units.keys():
#             for i in range(len(input_units[key])):
#                 pass

if __name__ == "__main__":
    main()
