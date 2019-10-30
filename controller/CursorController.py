#!/bin/env python
cursor = "x"
class CursorController:
    def setCursor(x):
        global cursor
        cursor = x
    def goDown():
        cursor.goDown()
    def goUp():
        cursor.goUp()
    def goLeft():
        cursor.goLeft()
    def goRight():
        cursor.goRight()
    def getCursor():
        return cursor.getCursor()
    def printCursor():
        cursor.printCursor()
    def setMaxArtist(x):
        cursor.setMaxArtist(x)
    def setMaxAlbum(x):
        cursor.setMaxAlbum(x)
    def setMaxSong(x):
        cursor.setMaxSong(x)
    def restartCursor():
        cursor.restartCursor()
