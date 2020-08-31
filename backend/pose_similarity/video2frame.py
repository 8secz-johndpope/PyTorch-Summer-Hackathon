import cv2
import argparse

parser = argparse.ArgumentParser(description='Convert frames to a video')
parser.add_argument('--frames', default='./images', type=str, help='video frames file')
parser.add_argument('--input', default='./video', type=str, help='input video name')
args = parser.parse_args()


vidcap = cv2.VideoCapture(args.input)
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite(args.frames + "/%s.jpg" % str(count).zfill(6), image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1