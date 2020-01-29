#!/bin/env python
import curses
import sys
from sys import stdin
import os
from controller import CursorController, ViewController, SpotifyController, MPDController
from view import View
from model import SpotifySearch, MPDclient, Cursor
stdscr= curses.initscr()
stdscr.keypad(True)

cr = CursorController.CursorController
cr.setCursor(Cursor.Cursor())
vc = ViewController.ViewController
mpd = MPDController.MPDController
mpd.connect(MPDclient.connect()) 
spot = SpotifyController.SpotifyController
spot.setSpotify(SpotifySearch)


def setAlbums(artist):
    searchResult[artist].albums = []
    searchResult[artist].albums = spot.setArtistAlbums(searchResult[artist]).albums
    cr.setMaxAlbum(len(searchResult[artist].albums))
    return searchResult

def setSongs(artist,album):
    searchResult[artist].albums[album].songs = []
    searchResult[artist].albums[album].songs = spot.setAlbumSongs(searchResult[artist].albums[album]).songs
    return searchResult

def refreshScreen(searchResult, cursor):
    if cursor.column == 1:
        searchResult = setAlbums(cursor.artist);
        vc.fillArtistsPad(searchResult, cursor)
        vc.fillAlbumsPad(searchResult[cursor.artist].albums, cursor)
        vc.fillInfoPad(searchResult[cursor.artist])
        cursor.setMaxArtist(len(searchResult))

    elif cursor.column == 2:
        searchResult = setSongs(cursor.artist, cursor.album);
        vc.fillAlbumsPad(searchResult[cursor.artist].albums, cursor)
        vc.fillSongsPad(searchResult[cursor.artist].albums[cursor.album].songs, cursor)
        cursor.setMaxAlbum(len(searchResult[cursor.artist].albums))
    elif cursor.column == 3:

        vc.fillSongsPad(searchResult[cursor.artist].albums[cursor.album].songs, cursor)
        cursor.setMaxSong(len(searchResult[cursor.artist].albums[cursor.album].songs))

def addToPlaylist(searchResult, cursor):
    global mpd
    if cursor.column == 1:
        mpd.addToPlaylist(searchResult[cursor.artist].uri)
    if cursor.column == 2:
        mpd.addToPlaylist(searchResult[cursor.artist].albums[cursor.album].uri)
    if cursor.column == 3:
        mpd.addToPlaylist(searchResult[cursor.artist].albums[cursor.album].songs[cursor.song].uri)

mpd.connect(MPDclient.connect()) 
vc.setView(View)
searchResult = spot.getFavourites()
refreshScreen(searchResult, cr.getCursor())

running = True
while(running):
    keypress = stdscr.getkey()
    if vc.checkResize() == True:
        vc.showSize()
        vc.resize()
    try: 
        if int(keypress) >= 1 & int(keypress) <= 9:
            multiplier = int(keypress)
            keypress = stdscr.getkey()
            try:
                if int(keypress) >= 1 & int(keypress) <= 9:
                    multiplier = multiplier*10 + int(keypress)
                    keypress = stdscr.getkey()
                else:
                    mutliplier = multiplier
            except:
                multiplier = multiplier

        else:
            multiplier = 1
    except:
        multiplier = 1

    
    #Key parser: 
    #Vim directional keys (hjkl)
    #y = search
    #F = add to favourites
    #f = see favourites
    #D = delete artist from favourites
    #a = Adds whatever is under the cursor to MPD playlist and starts playing
    #A = same as above, but starts from the first song of the album/artist
    #o = Deletes the current playlist and adds whatever is under the cursor to MPD playlist
    #s = stop
    #q = quit

    if keypress == "h":
        for i in range(0, multiplier):
            cr.goLeft()
        refreshScreen(searchResult, cr.getCursor())
    elif keypress == "k":
        for i in range(0, multiplier):
            cr.goUp()
        refreshScreen(searchResult, cr.getCursor())
    elif keypress == "l":
        for i in range(0, multiplier):
            cr.goRight()
        refreshScreen(searchResult, cr.getCursor())
    elif keypress == "j":
        for i in range(0, multiplier):
            cr.goDown()
        refreshScreen(searchResult, cr.getCursor())
    elif keypress == "a":
        cursor = cr.getCursor()
        if cursor.column == 1:
            mpd.add(searchResult[cursor.artist].uri)
        if cursor.column == 2:
            mpd.add(searchResult[cursor.artist].albums[cursor.album].uri)
        if cursor.column == 3:
            mpd.add(searchResult[cursor.artist].albums[cursor.album].songs[cursor.song].uri)
    elif keypress == "A":
        mpd.connect(MPDclient.connect()) 
        cursor = cr.getCursor()
        if cursor.column == 1:
            mpd.add(searchResult[cursor.artist].uri)
        if cursor.column == 2:
            mpd.add(searchResult[cursor.artist].albums[cursor.album].uri)
            mpd.playSongPos(-1 * len(searchResult[cursor.artist].albums[cursor.album].songs))
        if cursor.column == 3:
            mpd.add(searchResult[cursor.artist].albums[cursor.album].songs[cursor.song].uri)
            mpd.playSongPos(-1)
    elif keypress == "o" or keypress == "KEY_ENTER":
        mpd.connect(MPDclient.connect()) 
        mpd.clear()
        cursor = cr.getCursor()
        if cursor.column == 1:
            mpd.add(searchResult[cursor.artist].uri)
        if cursor.column == 2:
            mpd.add(searchResult[cursor.artist].albums[cursor.album].uri)
            mpd.playSongPos(0)
        if cursor.column == 3:
            mpd.add(searchResult[cursor.artist].albums[cursor.album].uri)
            mpd.playSongPos(cursor.song)
    elif keypress == "p":
        mpd.connect(MPDclient.connect()) 
        mpd.play()
    elif keypress == "s":
        mpd.connect(MPDclient.connect()) 
        mpd.pause()
    elif keypress == "y":
        entry = vc.getUserEntry()
        search = ''.join(chr(x) for x in entry)
        r = spot.searchArtist(search)
        if(r):
            cr.restartCursor()
            searchResult = r
            refreshScreen(searchResult, cr.getCursor())
        else: 
            print("No results")
            refreshScreen(searchResult, cr.getCursor())
    elif keypress == "r":
        searchResult = spot.getRelatedArtists(searchResult[cr.getCursor().artist]).relatedArtists
        cr.restartCursor()
        refreshScreen(searchResult, cr.getCursor())
    elif keypress == "q":
        running = False
    elif keypress == "D":
        favourites = spot.getFavourites()
        i = 0;
        for artist in favourites:
            if artist.name == searchResult[cr.getCursor().artist].name:
                try:
                    del favourites[i]
                except:
                    x = 1
            i +=1
        spot.setFavourites(favourites)
        favourites = spot.getFavourites()
        searchResult = favourites
        cr.restartCursor()
        refreshScreen(searchResult, cr.getCursor())
    elif keypress == "F":
        favourites = spot.getFavourites()
        favourites.append(searchResult[cr.getCursor().artist])
        spot.setFavourites(favourites)
    elif keypress == "f":
        searchResult = spot.getFavourites()
        cr.restartCursor()
        refreshScreen(searchResult, cr.getCursor())



