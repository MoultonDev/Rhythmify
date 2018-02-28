# Rhythmify
Command-line utility for converting iTunes playlists to Rhythmbox playlists

## Description

Rhythmify is a tool for converting an iTunes playlist into a Rhythmbox one. Given an exported .xml format iTunes playlist, it compares the data it pulls against the metadata from the music files in your library to generate the Rhythmbox .pls playlist file.

## Install

It's just a Python script, so download the file and put it wherever you like. If you don't have the Python Mutagen library installed, you will need to install it for the script to run. You can do so on Linux with one of the following commands:


```
python3 -m pip install mutagen
pip3 install mutagen
```

On a Debian-based distro it's available using apt:

```
sudo apt install python3-mutagen
```

## Example usage

The script takes as input an XML file and the directory you want it to check for music files:

```
$ rhythmify.py playlist.xml ~/moultondev/Music/
```
