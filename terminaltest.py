import threading

__author__ = 'Odd'
import argparse
import tvshowmover
import anime_mover


def mover():
    parser = argparse.ArgumentParser(description="Move and rename tv-shows")
    parser.add_argument('SOURCE', help="The directory to move files from")
    parser.add_argument('DESTINATION', help="The directory to move files to")
    parser.add_argument('-t', help="Thorough-mode, enables file length check", action='store_true')
    parser.add_argument('-a', help="Anime shows", action='store_true')
    args = vars(parser.parse_args())

    if args['a']:
        yielder = anime_mover.yield_files
        newname = anime_mover.newname_show
        moveshow = anime_mover.move_tvshow
    else:
        yielder = tvshowmover.yield_files
        newname = tvshowmover.newname_show
        moveshow = tvshowmover.move_tvshow

    for show in yielder(args['SOURCE'], True):
        print("Move '" + show + "'")
        try:
            print("to '" + args['DESTINATION'] + '/' + newname(show) + "'?")
        except TypeError:
            print("New name could not be generated, skipping...\n")
            continue
        reply = ""
        print("""Options:
        Yes, No, Cancel, Rename""")
        while reply not in ['y', 'n', 'c']:
            reply = input('Move? (y/n/c/r): ')
        print(reply)
        if reply == 'c':
            break
        elif reply == 'y':
            threading.Thread(target=moveshow(show, args['DESTINATION'])).run()
        elif reply == 'n':
            continue
        elif reply == 'r':
            newname = input("Type name of show")
            season_no = -1
            if not args['a']:
                season_no = input("Season number")
            episode_no = input("Episode number")
            threading.Thread(target=moveshow(renamed, args['DESTINATION'])).run()

if __name__ == '__main__':
    mover()