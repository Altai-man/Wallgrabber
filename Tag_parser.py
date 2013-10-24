#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Tag_parser.py
#
#  version 0.4
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
'''
   Docs(sorry for my English at all).
    This script is a part of Wallgrabber app. It can grab page with links on pictures
    from Konachan. Working only with Python 3.

    How to use:
        Run srcipt from terminal with command:
            $ python3 /way_to_script/Wallgrabber/Tag_parser.py
        Insert tags, which you wish to see on your wallpaper.
        Insert number of pages(so many of pictures, as many of pages).

    Script will download links on pictures to text file in directory, which named "/lists".

    Than you can use second part of script for downloading and installation
    or use lists create with Tag_parser with your own script. Enjoy.

    Main features:

       + Censored or uncut pictures.
       + Multi-tags.
       + Changeable number of pages to downoad.

    Functions:

          === main() - main script, used with all other func. Ask user
              for variables - tag and number of pages, than download pages,
              parse it, create text-file and write links.

          === page_grab(tag, [censored = 1], number) - download page from
              site and return HTML-source.
              First arg is a tag, which used for forming
              link, second is censure(for Konachan-only,
              maybe), third argument - number of pages to grab.

          === page_parsing(source_page) - parse HTML-page, returned by
              page_grab().
              Return list on links on pictures.
              First agr is variable, which point on string with source code.

          === file_creation(tag) - check file existing in directory.
              If true - ask user for permission to create new file.
              At 'y' answer from terminal - remove old file and create new.
              At 'n' answer - close script.
              If tag is new in directory /lists - create text file and return
              it. Name of file is always a tag - first arg.
              Return true(if file exists) or false(if file not exist).

    Variables:

       [*] PATTERN_KONA_PIC = regexp pattern for cutting first part of link.

       [*] PATTERN_KONA_PIC2 = regexp pattern for cutting second part of link.

       [*] tag = name, used in urls and name of files with lists.

       [*] page_code = raw HTML-page.

       [*] links_list = list of links on pictures.

'''


# Imports.

import os
import re
from urllib.request import urlopen


# Patterns.

PATTERN_KONA_PIC = re.compile('"jpeg_url":"(.*)",')
PATTERN_KONA_PIC2 = re.compile('(.*)","jpeg_width"')


# Consts.

KONA_WHITE = r'http://konachan.net/post?tags='  # Konachan without h-pictures.
KONA_BLACK = r'http://konachan.com/post?tags='  # Konachan with h-pictures.


# Functions.

def page_grab(tag, number, censored):
    '''
       === page_grab(tag, [censored = 1], [number=1]) - download page from
            Konachan(or whatever I write, hehe) and return
            HTML-source. First arg is a tag, which used for forming link,
            second is censure(for Konachan-only, maybe).
            third arg is number of downloading pages with links.
    '''
    if censored == 1:
        url = KONA_WHITE
    else:
        url = KONA_BLACK

    source_page = ''

    i = 1


    while i <= number:
        server_name = url + tag + '&page=' + str(i)
        pages_with_list = urlopen(server_name)
        source_page += str(pages_with_list.read().decode('utf-8'))
        print('I grab page ' + str(i) + '!')
        pages_with_list.close()
        if 'Nobody here but us chickens!' in source_page:
            print('Not enough pictures with this tag on server. Sorry.')
            break

        i += 1

    return source_page


def page_parsing(source_page):
    '''
       === page_parsing(source_page) - parse HTML-page using re-module,
           returned by page_grab().
           Return list on links on pictures. First agr is variable,
           which point on source of page.
    '''
    lines = re.findall(PATTERN_KONA_PIC, source_page)
    links_list = []

    while lines:
        link = re.match(PATTERN_KONA_PIC2, lines[0])
        link = link.group(1)
        links_list.append(link)
        lines = lines[1:]

    return links_list


def file_creation(tag):
    '''
       === file_creation(tag) - check file existing in directory.
           If true - ask user for permission to create new file.
           At 'y' answer from terminal - remove old file and create new.
           At 'n' answer - close script.
           If tag is new in directory /lists - create text file and return
           it. Name of file is always a tag - first arg.
           Return true(if file exists) or false(if file not exist).
    '''
    if tag in os.listdir():
        answ = input('List of pics with this tag is exist. '
                     + 'Create new list? y/n: ')
        if answ == 'y':
            os.remove(tag)
            file_for_link = open(tag, mode='w')

            return file_for_link

        elif answ == 'n':
            print('Exit.')
            exit()
        else:
            print('Unknown command.')
            exit()
    else:
        file_for_link = open(tag, mode='w')

        return file_for_link


def main():
    '''
        === main() - main script, used with all other func. No args.
    '''
    if 'lists' in os.listdir():
        os.chdir('lists')
    else:
        os.mkdir('lists')
        os.chdir('lists')

    print('''
          |-----Tag_parser-----|
          |Version: 0.3        |
          |Creator: deb-user   |
          |--------------------|
          ''')

    tag = input('Enter tags split by plus: ')  # Like 'fox+loli' or 'loli'

    file_for_links = file_creation(tag)

    num = int(input('How much pages you need to? '))
    censure = input('Are you needed hentai pictures? Y/N: ')
    if censure == 'Y':
        page_code = page_grab(tag, num, 0)  # This is a bycicle, Luke!
    elif censure == 'N':
        page_code = page_grab(tag, num, 1)
    else:
        print('Hey, choose right answer next time!')
        exit()

    links_list = page_parsing(page_code)

    count_pic = 0  # Variable for counting pictures.

    while links_list:
        file_for_links.write(links_list[0])
        file_for_links.write('\n')
        count_pic += 1
        links_list = links_list[1:]
    print('I grab ' + str(count_pic) + ' picture/s.')

    return 0


if __name__ == '__main__':

    main()
