import cv2
import time
import argparse
import os
import torch
import json
import sys

import posenet


parser = argparse.ArgumentParser()
parser.add_argument('--model', type=int, default=101)
parser.add_argument('--scale_factor', type=float, default=1.0)
parser.add_argument('--notxt', action='store_true')
parser.add_argument('--image_dir', type=str, default='./images')
parser.add_argument('--output_dir', type=str, default='./output')
args = parser.parse_args()


def main():
    model = posenet.load_model(args.model)
    model = model.cuda()
    output_stride = model.output_stride

    if args.output_dir:
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)

    filenames = [
        f.path for f in sorted(os.scandir(args.image_dir), key=lambda x: (x.is_dir(), x.name)) if f.is_file() and f.path.endswith(('.png', '.jpg'))]

    keypoints_list = {} #單一frame的所有keypoints

    start = time.time()
    for f in filenames:
        input_image, draw_image, output_scale = posenet.read_imgfile(
            f, scale_factor=args.scale_factor, output_stride=output_stride)

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

        if args.output_dir:
            draw_image = posenet.draw_skel_and_kp(
                draw_image, pose_scores, keypoint_scores, keypoint_coords,
                min_pose_score=0.25, min_part_score=0.25)

            cv2.imwrite(os.path.join(args.output_dir, os.path.relpath(f, args.image_dir)), draw_image)

        
        p1 = None
        p2 = None
        area = 0

        keypoints = []
        if not args.notxt:
            print()
            print("Results for image: %s" % f)
            for pi in range(len(pose_scores)):
                if pose_scores[pi] == 0.:
                    break

                index = 0
                max_x = 0
                max_y = 0
                min_x = 9999
                min_y = 9999
                temp_keypoints = dict()
                print('Pose #%d, score = %f' % (pi, pose_scores[pi]))
                for ki, (s, c) in enumerate(zip(keypoint_scores[pi, :], keypoint_coords[pi, :, :])):
                    print('Keypoint %s, score = %f, coord = %s' % (posenet.PART_NAMES[ki], s, c))
                    if pi == 0:
                        if(index > 4):
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
                    keypoints_list[f[-10:-4]] = keypoints
                    # keypoints_list['test'] = keypoints
                            
                
                # keypoints_list[f[-10:-4]] = keypoints


    print('Average FPS:', len(filenames) / (time.time() - start))

    result = dict()
    result[args.image_dir.split('/')[-1]] = keypoints_list
    ret = json.dumps(result)
    with open(args.image_dir.split('/')[-1]+'.json', 'w') as fp:
        fp.write(ret)

def video2frame(filename):
    video = []
    vidcap = cv2.VideoCapture(filename)
    success,image = vidcap.read()
    while success:
        # cv2.imwrite(args.frames + "/%s.jpg" % str(count).zfill(6), image)     # save frame as JPEG file    
        video.append(image)  
        success,image = vidcap.read()

    return video

if __name__ == "__main__":
    main()
