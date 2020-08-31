import os
import numpy as np
import cv2
import json
import argparse

parser = argparse.ArgumentParser(description='vote for most similar video')
parser.add_argument('--DB', default = './4database.json', type=str, help='json of DB video')
parser.add_argument('--image', default = './output/sample2', type=str, help='frames of test video')

def ReadJSON(path):
    with open(path, 'r') as f:
        DB_videos = json.load(f)
        f.close()
    return DB_videos

def main():
    args = parser.parse_args()
    DB_videos = ReadJSON(args.DB)

if __name__ == '__main__':
    main()

data = [
                [
                    149.25650312947823,
                    261.22193192171045
                ],
                [
                    148.20130721030088,
                    237.71023195358967
                ],
                [
                    151.64182744012678,
                    279.8278275369296
                ],
                [
                    136.63081614896868,
                    221.03463992685684
                ],
                [
                    145.69659739648316,
                    286.11409536947883
                ],
                [
                    120.46716679256969,
                    208.81782019938024
                ],
                [
                    184.4043397768361,
                    252.13215272995686
                ],
                [
                    180.8578818648125,
                    242.68104350883021
                ],
                [
                    209.79829699054318,
                    252.61689541678348
                ],
                [
                    210.9036222868533,
                    239.84637105706702
                ],
                [
                    243.91213230640963,
                    246.56077844676287
                ],
                [
                    238.68860839108908,
                    237.98458355265365
                ]
            ]