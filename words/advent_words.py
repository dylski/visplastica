import argparse
import datetime
import random


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--day", help="Override day")
ap.add_argument("-m", "--month", help="Override month")
ap.add_argument("-s", "--seed", help="Shuffle seed", default="123123")
ap.add_argument("-f", "--filename", help="Print filename instead of prompt", default=False, action='store_true')
ap.add_argument("-t", "--title", help="Print title instead of prompt", default=False, action='store_true')
args = vars(ap.parse_args())

date = args.get("day")
month  = args.get("month")
if date is not None:
    date = int(date)
if month is not None:
    month = int(month)

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
        "fairy on a Christmas tree",
        "snowman on a winter day",
        "Christmas cards",
        "mistletoe",
        "burning candle",
        "snow covered village",
        "baby Jesus in a manger",
        "a stable with a donkey",
        "holy star shining in the dark sky",
        "three wise men",
        "snowflake",
        "Father Christmas, Santa Claus",
        "reindeer and sleigh flying through the night past the moon",
        ]

twelve_days = [  # prompt, filename, title
        ["a partridge in a pear tree", "a_partridge_in_a_pear_tree", "A partridge in a pear tree"],
        ["two turtle doves", "two_turtle_doves", "Two turtle doves"],
        ["three French hens", "three_French_hens", "Three French hens"],
        ["four calling birds", "four_calling_birds", "Four calling birds"],
        ["five gold rings", "five_gold_rings", "Five gold rings"],
        ["six geese a-laying", "six_geese_a_laying", "Six geese a-laying"],
        ["seven swans a-swimming", "seven_swans_a_swimming", "Seven swans a-swimming"],
        ["eight maids a-milking", "eight_maids_a_milking", "Eight maids a-milking"],
        ["nine ladies dancing", "nine_ladies_dancing", "Nine ladies dancing"],
        ["ten lords a-leaping", "ten_lords_a_leaping", "Ten lords a-leaping"],
        ["eleven pipers piping", "eleven_pipers_piping", "Eleven pipers piping"],
        ["twelve drummers drumming", "twelve_drummers_drumming", "Twelve drummers drumming"]]

special_nouns = ["Christmas day has arrived",
        "It is Boxing day",
        "The aftermath",
        "A walk in the winter wonderland",
        "Hot toddies and mulled wine with friends",
        "Keeping cosy and warm by the fire",
        "New Years Eve",
        #"New Years Day",
        #"Back to work"
        ]

subjects = [
        "The Soul",
        "The Moon is Made of Cheese",
        "The Earth is Flat",
        "Aliens Under the Sea Having a Picnic",
        "Dogs Playing Chess",
        "A Cat on a Bicycle in the Rain",
        "Kitten Sandwich",
        "Working From Home",
        "The Face of Darkness in the Clouds",
        "A Jellyfish Playing Soccer",
        "An Octopus Wearing Boots",
        "Pigeons in the Office",
        "A Galaxy of Opportunity",
        "An AI Dreaming of Conciousness",
        "A Zoo Party",
        "Earth in Danger, Act Fast",
        "Choose Love",
        "Climate Warming, Seas Rising",
        "Corruption Everywhere",
        "Inside the Brain of an AI",
        "A Brain Made of Neurons in Space",]

artists = [
        "Salvador Dali",
        "Rembrandt",
        "Vincent van Gogh",
        "Michelangelo",
        "Leonardo da Vinci",
        "Miquel Barcelo",
        "Cecily Brown",
        "Cindy Sherman",
        "Liu Xiaodong",
        "Luo Zhongli",
        "Mark Bradford",
        "Albert Oehlen",
        "Anselm Kiefer",
        "Adrian Ghenie",
        "Zeng Fanzhi",
        "Keith Haring",
        "Yoshitomo Nara ",
        "Jean-Michel Basquiat",
        "Peter Doig",
        "Christopher Wool",
        "Mark Grotjahn",
        "Richard Prince",
        "Rudolf Stingel",
        "Damien Hirst",
        "George Condo",
        "Jeff Koons",
        "Zhou Chunya",
        "Njideka Akunyili Crosby",
        "Günther Förg",
        "Takashi Murakami",
        "Liu Wei",
        "Sean Scully",
        "Thomas Schütte",
        "Zhang Xiaogang",
        "John Currin",
        "Paul Cezanne",
        "Andy Warhol",
        "Mark Rothko",
        "Wassily Kandinsky",
        "Jackson Pollock",
        "Piet Mondrian",
        "Paul Gauguin",
]


random.Random(seed).shuffle(nouns)
random.Random(seed).shuffle(subjects)
random.Random(seed).shuffle(artists)


if date is None:
    date = int(datetime.datetime.now().strftime("%d"))
if month is None:
    month = int(datetime.datetime.now().strftime("%m"))
 
if month == 12 and date < 25:
    if title:
        print(f"Advent day {date}")
        exit()
    if filename:
        timestamp = datetime.datetime.now().now().strftime("%Y%m%d%H%M%S")
        print(f"advent_day_{date}_{timestamp}")
        exit()

    date -= 1
    if date < len(nouns):
        prompt = nouns[date]
    else:
        spec = date - len(nouns)
        if spec < len(special_nouns):
            prompt = special_nouns[spec]
    print("photorealistic " + prompt)
    exit()

if month == 12:
    if title:
        print(twelve_days[date - 25][2])
        exit()

    if filename:
        timestamp = datetime.datetime.now().now().strftime("%Y%m%d%H%M%S")
        print(f"twelve_days_{date - 24}_{timestamp}")
        exit()

    print(twelve_days[date - 25][0])
    exit()

if title:
    print(twelve_days[date + 6][2])
    exit()

if filename:
    timestamp = datetime.datetime.now().now().strftime("%Y%m%d%H%M%S")
    print(f"twelve_days_{date + 7}_{timestamp}")
    exit()

print(twelve_days[date + 6][0])
