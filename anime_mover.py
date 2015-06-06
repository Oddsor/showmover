from tvshowmover import enclose_regs

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
    basename = os.path.splitext(filename)[0]
    no_encloses = ""
    for enclose in tvshowmover.enclose_regs:
        no_encloses = re.sub(enclose, "", basename).strip()
    showname = get_value_from_pattern(no_encloses, tvshowmover.title_regs, 'Title')
    ep_number = get_value_from_pattern(no_encloses, tvshowmover.episode_regs, 'Episode')
    #ep_title = get_value_from_pattern(no_encloses, tvshowmover.eptitle_regs, 'Ep-title')
    ep_title = ""
    return showname + "\\" + showname + " - " + ep_number + (" - " + ep_title if ep_title != "" else "") +\
        tvshowmover.get_fileending(filename)


def get_value_from_pattern(filename, pattern_list, data_type='Title'):
    filename = re.sub("\.|_", " ", filename)
    value = ""
    for pattern in pattern_list:
        print(str(re.search(pattern, filename, flags=re.IGNORECASE)))
        if re.search(pattern, filename, flags=re.IGNORECASE) is None:
            continue
        suggestion = re.search(pattern, filename, flags=re.IGNORECASE).group(0).strip()
        print(data_type + ": " + suggestion)
        command = input("r to retry, s to skip:")
        if command == 'r':
            continue
        elif command == 's':
            return ""
        else:
            value = suggestion
            break
    if value == "":
        value = input("Missing value " + data_type + ", add:")
    return value


def move_tvshow(source, destination, newfile):
    os.makedirs(destination + "\\" + newfile.split("\\")[0], exist_ok=True)
    shutil.move(source, destination + "\\" + newfile)

if __name__ == '__main__':
    print('\n'.join([x for x in yield_files('F:/Torrent', True)]))