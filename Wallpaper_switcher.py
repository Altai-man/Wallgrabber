#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Wallpaper_switcher.py
#
#  version 0.2
#
#  Copyright 2013 deb-user <deb-user@debian>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


"""
   Docs.
    This script is a part of Wallgrabber app.

    Functions:
        === opening(tag) - open and read file with name = first arg.

        === randomize_wall(list_of_pic) - choose  pic, remove '/' from link.

        === down_wall(picture) - download picture from link in str-agr and
            write it to path of dir with script.

    Variables:

        [*] dir = dir with script.

        [*] tag = name of file with list.

        [*] list_of_pic = list of strings with links from tag-file.

        [*] picture = link on random picture from list.

"""

# Imports.

import os
import random
import urllib.request
import Config
tag = Config.tag

# Functions.

def down_wall(picture):
    '''
       === down_wall(picture) - download picture from link in str-agr and
           write it to path of dir with script.
    '''
    if 'tmpwall.jpg' in os.listdir():

        os.remove('tmpwall.jpg')
        pic = open('tmpwall.jpg', 'wb')
        pic.write(urllib.request.urlopen(picture).read())
        pic.close()

        os.remove('checker')

        check = open('checker', 'w')
        check.write(picture)
        check.close()

    else:

        pic = open('tmpwall.jpg', 'wb')
        pic.write(urllib.request.urlopen(picture).read())
        pic.close()

        check = open('checker', 'w')
        check.write(picture)
        check.close()

        return 0


def randomize_wall(list_of_pic):
    '''
       === randomize_wall(list_of_pic) - choose  pic, remove '/' from link.
    '''
    if Config.check_able == True:
        os.chdir('..')
        checker = open('checker', 'r')
        used = checker.read()
        checker.close()

        for item in list_of_pic:
            if used == item:
                list_of_pic.pop(list_of_pic.index(used))
            else:
                pass
        picture = random.choice(list_of_pic)

    elif Config.check_able == False:
        picture = random.choice(list_of_pic)

    new_s = ''

    for char in picture:

        if char != "\\":

            new_s += char

        else:

            new_s += ''

    return new_s


def opening(tag):
    '''
        === opening(tag) - open and read file with name = first arg.
    '''
    os.chdir('.wallgrabber/lists')

    if Config.tag in os.listdir():
        file_with_list = open(Config.tag, mode='r')
        list_of_pic = file_with_list.readlines()
        return list_of_pic

    else:
        print('List does not exist. At first create list with Page_grabber.py!')
        exit()


def main():
    '''
       === main() - main script, which used all other func. No args.
    '''
    # Open list with pics.
    list_of_pic = opening(Config.tag)
    # Choose random pic.
    picture = randomize_wall(list_of_pic)
    # Dowload pic.
    down_wall(picture)
    # Set string.
    string_to_exec = ('DISPLAY=:0.0 && feh --bg-scale '
                      + Config.directory + '/tmpwall.jpg')
    os.system(string_to_exec)

if __name__ == '__main__':
    main()
