#!/usr/bin/env python3

# Rhythmify
# Author: MoultonDev
#
# A utility for converting iTunes playlists into Rhythmbox playlists

from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4
import os
import sys
import xml.etree.ElementTree as ETree

def main():
    if len(sys.argv) < 3:
        print('usage: rhythmify <itunes playlist> <music library>')
        sys.exit()

    xmlfile = sys.argv[1]
    playlist_name = xmlfile.split('.')[0]
    path = sys.argv[2]

    xmltree = ETree.parse(xmlfile)
    xmlroot = xmltree.getroot()

    xmlsongs = xmlroot[0][17]
    xmlplaylist = xmlroot[0][19][0][11]

    playlist = []
    for id in xmlplaylist:
        playlist.append(id[1].text)

    # xmlsongs is formatted with a series of consecutive tags where tag N is a
    # key for tag N+1, so the following loop makes that useful
    i = 0
    songdict = {}
    while i < len(xmlsongs):
        # the data in each xmlsongs value has the same structure
        j = 0
        temp = {}
        while j < len(xmlsongs[i+1]):
            temp[xmlsongs[i+1][j].text] = xmlsongs[i+1][j+1].text
            j += 2
        songdict[xmlsongs[i].text] = temp
        i += 2

    # now the values in playlist can be used as keys to songdict

    # main loop
    with open('{}.pls'.format(playlist_name), 'w') as out_file:
        out_file.write('[playlist]\n')
        out_file.write('X-GNOME-Title={}\n'.format(playlist_name))
        out_file.write('NumberOfEntries={}\n'.format(len(playlist)))
        
        # build song list once
        songfiles = []
        for root, _, files in os.walk(path):
            for file in files:
                ext = file.split('.')[-1]
                if ext == 'mp3' or ext == 'm4a' or ext == 'mp4':
                    songfiles.append('{}/{}'.format(root, file))
        
        print(len(songfiles))
        print(len(playlist))
        input('acknowledgethis')

        index = 1 # file count in rhythmbox playlist
        for songid in playlist:
            meta_itunes = songdict[songid]
            for song in songfiles:
                print('{} by {}\n'.format(title, artist))
                if song.split('.')[-1] == 'mp3':
                    meta = EasyID3(song)
                    if 'albumartist' in meta:
                        artist = meta['albumartist'][0]
                    else:
                        artist = meta['artist'][0]
                    if 'title' not in meta:
                        continue
                    title = meta['title'][0]
                else: # mp4 / m4a
                    meta = MP4(song).tags
                    if 'aART' in meta:
                        artist = meta['aART'][0]
                    else:
                        artist = meta['\xa9ART'][0]
                    if '\xa9ART' not in meta:
                        continue
                    title = meta['\xa9nam'][0]
            
                if artist == meta_itunes['Artist'] and title == meta_itunes['Name']:
                    out_file.write('File{}=file://{}\n'.format(index, song))
                    out_file.write('Title{}={}\n'.format(index, title))
                    index += 1 # we've added a song to the playlist
                    break

if __name__=='__main__':
    main()