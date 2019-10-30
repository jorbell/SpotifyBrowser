#!/bin/env python
import curses
import os
import sys
import subprocess
#import SpotifySearch as ss

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()

stdscr.keypad(True)
artistPad = curses.newpad(100,int(curses.COLS/3))
albumPad = curses.newpad(100,int(curses.COLS/3))
songPad = curses.newpad(100,int(curses.COLS/3))
infoPad = curses.newpad(10,curses.COLS)
padwidth = int(curses.COLS/3)
"""
begin_x = 20
begin_y = 10
height = curses.LINES
width = curses.COLS
win = curses.newwin(height, width, begin_y, begin_x)
"""

stdscr.refresh()

def showSize():
    global padwidth
    padwidth = int(curses.COLS/3)
    infoPad.addstr(5,0,"COLS:"+str(curses.COLS),curses.A_NORMAL)
    infoPad.addstr(6,0,"Rows:"+str(curses.LINES),curses.A_NORMAL)
    infoPad.addstr(7,0,"Padwidth:"+str(padwidth),curses.A_NORMAL)
    y, x = stdscr.getmaxyx()
    #infoPad.addstr(5,30,"X:"+str(x),curses.A_NORMAL)
    #infoPad.addstr(6,30,"Y:"+str(y),curses.A_NORMAL)
    stdscr.refresh()
    curses.COLS = x
    curses.LINES = y
    padwidth = int(curses.COLS/3)
    #infoPad.addstr(5,60,"COLS:"+str(curses.COLS),curses.A_NORMAL)
    #infoPad.addstr(6,60,"Rows:"+str(curses.LINES),curses.A_NORMAL)
    #infoPad.addstr(7,60,"Padwidth:"+str(padwidth),curses.A_NORMAL)
def resize():
    #curses.KEY_RESIZE
    padwidth = int(curses.COLS/3)
    y, x = stdscr.getmaxyx()
    #curses.resize_term()
    stdscr.clear()
    showSize()
    refreshPads()
def checkResize():
    y, x = stdscr.getmaxyx()
    if int(curses.COLS) != x:
        return True
    if int(curses.LINES) != y:
        return True

def refreshPads(): 
#                     start, from, to
#                     y,x  y,x  y,x
    artistPad.refresh(0,0, 10,0, curses.LINES-1,50)
    albumPad.refresh(0,0, 10,padwidth, curses.LINES-1,300)
    songPad.refresh(0,0, 10,padwidth*2, curses.LINES-1,300)
    infoPad.refresh(0,0,0,0,9,curses.COLS)
    #x=1

def fillArtistsPad(artists, cursor):
    i = 0
    while (i< 50):
            artistPad.addstr(i,0,"                                                                          ", curses.A_NORMAL)
            i += 1
    i = 1;
    artistPad.addstr(0,0,"Artist:           ", curses.A_NORMAL)
    for artist in artists:
        artistPad.addstr(i,0,chr(9553), curses.A_NORMAL)
        if cursor.artist == i-1:
            artistPad.addstr(i,1,artist.name, curses.A_REVERSE)
        else:
            artistPad.addstr(i,1,artist.name, curses.A_NORMAL)
        i += 1;
    #artistPad.refresh(0,0, 10,0, (curses.LINES-1),50)
    if (cursor.artist > curses.LINES -12 ):
        artistPad.refresh(cursor.artist - (curses.LINES - 12),0, 10,0, (curses.LINES-1),50)
    else:
        artistPad.refresh(0,0, 10,0, (curses.LINES-1),50)


def fillAlbumsPad(albums, cursor):
    i= 1;
    #flushPad(albums, albumPad)
    while (i< 50):
            albumPad.addstr(i,0,"                                                                          ", curses.A_NORMAL)
            i += 1
    i = 1;
    albumPad.addstr(0,0,"Album:", curses.A_NORMAL)
    for album in albums:
        albumPad.addstr(i,0,chr(9553), curses.A_NORMAL)
        if cursor.album == i-1:
            albumPad.addstr(i,1,albums[i-1].name, curses.A_STANDOUT)
        else: 
            albumPad.addstr(i,1,albums[i-1].name, curses.A_NORMAL)
        i += 1;
    if (cursor.album > curses.LINES -12 ):
        albumPad.refresh(cursor.album - (curses.LINES -12),0, 10,padwidth, (curses.LINES-1),300)
    else:
        albumPad.refresh(0,0, 10,padwidth, (curses.LINES-1),300)

def fillSongsPad(songs, cursor):
    i= 0;
    #songPad.addstr(i,0,songs[1].name, curses.A_STANDOUT)
    while (i<50):
        songPad.addstr(i,0,"                                                                              ", curses.A_NORMAL)
        i += 1
    i = 1;
    songPad.addstr(0,0,"Song:", curses.A_NORMAL)
    for song in songs:
        songPad.addstr(i,0,chr(9553), curses.A_NORMAL)
        if cursor.song == i-1:
            songPad.addstr(i,1,song.name, curses.A_STANDOUT)
        else:
            songPad.addstr(i,1,song.name, curses.A_NORMAL)
        i += 1;
    if (cursor.song > curses.LINES -12 ):
        songPad.refresh(cursor.song - (curses.LINES -12),0, 10,padwidth*2, (curses.LINES-1),300)
    else:
        songPad.refresh(0,0, 10,padwidth*2, (curses.LINES-1),300)
def fillInfoPad(artist):
    i = 0;
    while (i< 5):
        infoPad.addstr(i,0,"                                                                          ", curses.A_NORMAL)
        i += 1

    infoPad.addstr(1,0,"Artist: "+artist.name,curses.A_NORMAL)
    infoPad.addstr(2,0,"Followers: "+str(artist.followers),curses.A_NORMAL)
    infoPad.addstr(3,0,"",curses.A_NORMAL)

    infoPad.refresh(1,0,0,0,9,curses.COLS)


def flushPad(list, pad):
    for item in list:
        pad.addStr(i,0,chr(' ') *curses.COLS, curses.A_NORMAL)
def getUserEntry():
    stdscr.addstr(9,0,"Search:                                                       ",curses.A_NORMAL)
    curses.echo()
    entry = stdscr.getstr(9,7, 40)
    #stdscr.addstr(9,0,"Search:",curses.A_NORMAL)
    curses.noecho()
    return entry

def start():

    infoPad.addstr(0,0,"Jooo", curses.A_STANDOUT)
    refreshPads()
