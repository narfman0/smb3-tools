#! /usr/bin/env python3
"""
Description: Offset smb3 warpless splits by about 17s each world to accomodate
offscreen wand grabs.
Elaboration: Generally SMB3 runners split when we touch the wand, however,
when we get offscreen wand grabs the split is very inaccurate. So, it is preferable
to split instead on a consistent time, liuke when the king grabs the wand after
all the OSWG action occurs and the runner can accurately split. Change is tough
though since the runner has already split for ages using the old method, so we want
to automate changing those legacy splits. This script performs those offset changes
automatically. 
Author: lui
copied on 2023-02-27
"""

import datetime
import re
import sys
import xml.etree.ElementTree as ET

# TODO pass this as an argument?
split_on_peachs_letter = True
frames_between_king_wand_grab_and_peachs_letter_w1 = 858
frames_between_king_wand_grab_and_peachs_letter_w2 = 865  # of course they are different, lets just pick one in the middle and pretend its average
peachs_letter_additional_s = (
    frames_between_king_wand_grab_and_peachs_letter_w2 * 0.01664
)

# start: 0
# world 1: 122157 - 121098 = 1059 = 17.638s
# world 2: 146415 - 145352 = 1063 = 17.704s (+1 tile)
# world 3: 178130 - 177075 = 1055 = 17.571s
# world 4: 204575 - 203508 = 1067 = 17.771s (+2 tiles)
# world 5: 239995 - 238932 = 1063 = 17.704s (+1 tile)
# world 6: 279565 - 278513 = 1052 = 17.521s
# world 7: 321765 - 320706 = 1059 = 17.638s (+1 tile)
# world 8: 0
deltas = [0, 17.638, 17.704, 17.571, 17.771, 17.704, 17.521, 17.638, 0]

if split_on_peachs_letter:
    deltas = [
        delta + peachs_letter_additional_s if delta else delta for delta in deltas
    ]


def get_time(time_element):
    t = re.sub(r"(?<=\.\d\d\d)0000", "000", time_element.text)
    t = re.sub(r"(:\d\d)$", r"\1.000000", t)

    # strptime only supports 6 numerals after the decimal
    dot_index = t.find(".")
    if dot_index < len(t) - 7:
        t = t[0 : dot_index + 7]

    return datetime.datetime.strptime(t, "%H:%M:%S.%f")


def set_time(time_element, time):
    time_element.text = datetime.datetime.strftime(time, "%H:%M:%S.%f")


# main
help_args = ["-h", "--h", "-help", "--help", "-?", "--?"]
if (len(sys.argv) == 2 and sys.argv[1] in help_args) or len(sys.argv) > 3:
    print("usage: offsetsplits.py lss_file [output]")
    exit()

if len(sys.argv) == 1:
    infile = input("Enter splits file name: ")
else:
    infile = sys.argv[1]

if len(sys.argv) == 3:
    outfile = sys.argv[2]
elif "." in infile:
    outfile = ".".join(infile.split(".")[:-1]) + "_out." + infile.split(".")[-1]
else:
    outfile = infile + "_out"

tree = ET.parse(infile)
root = tree.getroot()

for world, segment in enumerate(root.find("Segments"), start=1):
    dt_split = datetime.timedelta(seconds=deltas[world])
    dt_segment = datetime.timedelta(seconds=deltas[world] - deltas[world - 1])
    for split_time in segment.find("SplitTimes"):
        t = get_time(split_time.find("RealTime"))
        set_time(split_time.find("RealTime"), t + dt_split)
    best_segment_time = segment.find("BestSegmentTime")
    t = get_time(best_segment_time.find("RealTime"))
    set_time(best_segment_time.find("RealTime"), t + dt_segment)
    for segment_time in segment.find("SegmentHistory"):
        if segment_time.find("RealTime") != None:
            t = get_time(segment_time.find("RealTime"))
            set_time(segment_time.find("RealTime"), t + dt_segment)

tree.write(outfile)
