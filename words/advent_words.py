import argparse
import datetime
import random


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--date", help="Override date (day number)")
ap.add_argument("-s", "--seed", help="Shuffle seed", default="4")
ap.add_argument("-f", "--filename", help="Print filename instead of prompt", default=False, action='store_true')
ap.add_argument("-t", "--title", help="Print title instead of prompt", default=False, action='store_true')
args = vars(ap.parse_args())

date = args.get("date")
if date is not None:
    date = int(date)
seed = int(args.get("seed"))
filename = args.get("filename")
title = args.get("title")

nouns = ["Christmas tree",
        "Christmas wreath",
        "holly berries and leaves with snow",
        "Christmas baubles",
        "Christmas pudding",
        "Christmas cake with icing and Christmas scene on top",
        "Christmas presents",
        "Christmas stocking hanging in front of a fireplace",
        "Christmas sleigh",
        "Rudolf the red-nosed reindeer",
        "Christmas bells",
        "Christmas tree fairy",
        "snowman",
        "Christmas cards",
        "mistletoe",
        "burning candle",
        "snow covered village",
        "baby Jesus in a manger",
        "a stable with a donkey",
        "holy star shining in the dark sky",
        "three wise men",
        "christmas winter snow covered village",
        "Father Christmas, Santa Claus",
        "reindeer and sleigh flying through the night past the moona",
        ]

if date is None:
    date = int(datetime.datetime.now().strftime("%d"))

if filename or title:
    if title:
        print(f"Advent calendar day {date}")
    if filename:
        print(f"advent_day_{date}")
    exit()

shuffled = list(nouns)
random.Random(seed).shuffle(shuffled)
print(shuffled[(date % len(shuffled))])

