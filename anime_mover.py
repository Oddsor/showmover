__author__ = 'Odd Andreas Sørsæther'

import tvshowmover
import re
import os
import shutil


def is_anime(filename):
    return len(re.findall("\[\w+\].*?\d{1,2}.*(mkv|avi|mp4)", filename, flags=re.IGNORECASE)) > 0


def is_video(filename):
    return os.path.splitext(filename)[1] in ['.mkv', '.mp4', '.avi']


def yield_files(directory, subfolders=True, thorough=False):
    entries = os.listdir(directory)
    for item in entries:
        if os.path.isdir(directory + "/" + item) and subfolders:
            for x in yield_files(directory + "/" + item, subfolders=True, thorough=thorough):
                yield x
        elif not thorough:
            if is_anime(item):
                yield directory + "/" + item
            #elif is_anime(directory + "/" + item):
            #    yield directory + "/" + item
        else:
            try:
                if is_video(item):
                    length = tvshowmover.video_length(directory + "/" + item)
                    if tvshowmover.to_seconds("26:00") > length > tvshowmover.to_seconds("18:00"):
                        yield directory + "/" + item
            except AttributeError:
                pass


def newname_show(source):
    filename = os.path.basename(source)
    if is_anime(filename):
        showname = get_showname(os.path.splitext(filename)[0])
        return showname + "\\" + showname + " - " + get_episodenumber(filename) + tvshowmover.get_fileending(filename)


def get_showname(filename):
    dottedname = re.sub("(\s|\.)(S[0-9]{2,3}E[0-9]{2,3}|[0-9]{1,2}x[0-9]{2,3}).*", "", filename, flags=re.IGNORECASE)
    removed_braces = re.sub("\[.*?\]", "", dottedname, flags=re.IGNORECASE)
    split_dash = re.split("-", removed_braces)
    if len(split_dash) > 1:
        del split_dash[-1]
    trimmed = [x for x in split_dash]
    return re.sub("[.|_]", " ", ("-".join(trimmed))).strip()


def get_episodenumber(filename):
    dottedname = re.sub("(\s|\.)(S[0-9]{2,3}E[0-9]{2,3}|[0-9]{1,2}x[0-9]{2,3}).*", "", filename, flags=re.IGNORECASE)
    removed_braces = re.sub("\[.*?\]", "", dottedname, flags=re.IGNORECASE)
    last_numbers = re.findall("\d{2}", removed_braces)
    if last_numbers:
        return last_numbers[-1]
    return False


def move_tvshow(source, destination):
    newpath = os.path.split(newname_show(source))
    os.makedirs(destination + "\\" + newpath[0], exist_ok=True)
    shutil.move(source, destination + "\\" + newpath[0] + "\\" + newpath[1])

if __name__ == '__main__':
    print('\n'.join([x for x in yield_files('F:/Torrent', True)]))