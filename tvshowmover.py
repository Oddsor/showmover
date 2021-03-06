__author__ = 'Odd Andreas Sørsæther'

import re
import os
import shutil
import configparser
import subprocess


title_regs = [
    ".*?((?=\s-\s\d{2})|(?=\dx\d{2}\D)|(?=S\d{2}))",  # Any char before a season-number or standalone episode numbers
    ".+(?=\s-)",  # Any chars before (- ##)
    ".*?((?=\(\d{4}\))|(?=\D\d{4}(?!x|p|\d)))"  # Any char before a year
]

season_regs = [
    "(?<=S)\d{1,2}(?!\d)",  # Numbers after an S
    "\d{1,2}(?=x\d{2}\D)",  # Number before an x followed by no more than two numbers
]

episode_regs = [
    "(?<=E)\d{2}(?!\d)",  # Number behind an E (episode)
    "(?<=x)\d{2}(?!\d)",  # Number behind an x (SxEE format)
    "(?<!\d)\d{2}(?!\d|\w)"  # Two numbers with no number before and no char behind
]

year_regs = [
    "(?<=\s|\()\d{4}(?=\s|\))"
]

enclose_regs = [
    "(\[|\().+?(\]|\))"
]

resolution_regs = [
    "((?<=\d{4}x)(\d{4}|\d{3}))|\d{3,4}p"
]

eptitle_regs = [
    "(?<=\d{2}\s-\s)(\w|\s|,|'|`|-)+"
]


def is_show(filename):
    return len(re.findall("(S[0-9]{2,3}E[0-9]{2,3}|[0-9]{1,2}x[0-9]{2,3}).*(mkv|mp4|avi)",
                          filename, flags=re.IGNORECASE)) > 0


def get_showname(filename):
    dottedname = re.sub("(\s|\.)(S[0-9]{2,3}E[0-9]{2,3}|[0-9]{1,2}x[0-9]{2,3}).*", "", filename, flags=re.IGNORECASE)
    return dottedname.replace(".", " ")


def get_season(filename):
    if is_show(filename):
        reg = re.findall("(S[0-9]{2,3}E[0-9]{2,3}|[0-9]{1,2}x[0-9]{2,3})",
                         filename, flags=re.IGNORECASE)[0]
        reg2 = re.sub("(E[0-9]{2,3}|x[0-9]{2,3}).*", "", reg, flags=re.IGNORECASE)
        reg3 = re.sub("(S(0)*|^0)", "", reg2, flags=re.IGNORECASE)
        return reg3
    return False


def get_fileending(filename):
    return os.path.splitext(filename)[1]


def get_episodenumber(filename):
    if is_show(filename):
        reg = re.findall("(S[0-9]{2,3}E[0-9]{2,3}|[0-9]{1,2}x[0-9]{2,3})",
                         filename, flags=re.IGNORECASE)[0]
        reg2 = re.sub("(S[0-9]{1,2}E|[0-9]{1,2}x)", "", reg, flags=re.IGNORECASE)
        return reg2
    return False


def get_showfiles(directory, subfolders=True):
    entries = os.listdir(directory)
    itemlist = []
    for item in entries:
        if os.path.isdir(directory + "\\" + item) and subfolders:
            diritems = get_showfiles(directory + "\\" + item, subfolders=True)
            if len(diritems) > 0:
                for subitem in diritems:
                    itemlist.append(subitem)
        elif is_show(item):
            itemlist.append(directory + "\\" + item)
        elif is_show(directory + "\\" + item):
            itemlist.append(directory + "\\" + item)
    return itemlist


def yield_files(directory, subfolders=True, thorough=False):
    entries = os.listdir(directory)
    for item in entries:
        if os.path.isdir(directory + "/" + item) and subfolders:
            for x in yield_files(directory + "/" + item, subfolders=True):
                yield x
        elif is_show(item):
            yield directory + "/" + item
        elif is_show(directory + "/" + item):
            yield directory + "/" + item


def video_length(filename):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    ffmpeg = config.get('DEFAULT', 'ffmpeg')
    ffmpeg_info = subprocess.getoutput(ffmpeg + " -i \"" + filename + "\"")
    result = re.search("Duration:\s.*?,", ffmpeg_info, re.DOTALL)
    duration = result.group(0)
    return to_seconds(duration.replace("Duration: ", "").replace(",", ""))


def to_seconds(duration_string):
    duration = duration_string.split(".")[0].split(":")
    seconds = 0
    counter = 0
    for i in range(len(duration) - 1, -1, -1):
        seconds += int(duration[i]) * (60 ** counter)
        counter += 1
    return seconds


def print_files(dire):
    itemlist = get_showfiles(dire)
    for item in itemlist:
        print(item)


def newname_show(source):
    filename = os.path.basename(source)
    if is_show(filename):
        showname = get_showname(filename)
        season = get_season(filename)
        if int(season) >= 10:
            double = True
        else:
            double = False
        return (showname + "\\Season " + season + "\\" + showname + " - " + ("S" if double else "S0") + season + "E"
                + get_episodenumber(filename) + get_fileending(filename))
    elif is_show(source):
        filefolder = os.path.split(os.path.split(source)[0])[1]
        showname = get_showname(filefolder)
        season = get_season(source)
        if int(season) >= 10:
            double = True
        else:
            double = False
        return (showname + "\\Season " + season + "\\" + showname + " - " + ("S" if double else "S0") + season
                + "E" + get_episodenumber(source) + os.path.splitext(filename)[1])


def move_tvshows(source, destination):
    tvshows = get_showfiles(source)
    for showfile in tvshows:
        newpath = os.path.split(newname_show(showfile))
        os.makedirs(destination + "\\" + newpath[0], exist_ok=True)
        shutil.move(showfile, destination + "\\" + newpath[0] + "\\" + newpath[1])


def move_tvshow(source, destination, newfile):
    os.makedirs(destination + "\\" + "\\".join(newfile.split("\\")[:-1]), exist_ok=True)
    shutil.move(source, destination + "\\" + newfile)


if __name__ == '__main__':
    fils = yield_files('F:/Torrent')
    print(fils.__next__())
    print(fils.__next__())