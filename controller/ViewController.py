#!/bin/env python
view = "x"
class ViewController:
    global view 
    view = "x"
    def setView(x):
        global view
        view = x
    def start():
        global view
        view.start()
    def refreshPads():
        global view
        view.refreshPads()
    def fillInfoPad(artist):
        global view
        view.fillInfoPad(artist)
    def fillSongsPad(songs, cursor):
        global view
        view.fillSongsPad(songs, cursor)
    def fillAlbumsPad(albums, cursor):
        global view
        view.fillAlbumsPad(albums, cursor)
    def fillArtistsPad(artists, cursor):
        global view
        view.fillArtistsPad(artists, cursor)
    def refreshPads():
        global view
        view.refreshPads()
    def getUserEntry():
        global view
        return view.getUserEntry()
    def resize():
        global view
        view.resize()
    def showSize():
        global view
        view.showSize()
    def checkResize():
        global view
        return view.checkResize()

