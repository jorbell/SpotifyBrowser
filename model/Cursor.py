#!/bin/env python

artist = 0
album = 0
song = 0
column = 1
class Cursor:
    MAX_artist = ""
    MAX_album = ""
    MAX_song = ""
    artist = 0
    album = 0
    song = 0
    column = 1

    def setMaxArtist(self, x):
        self.MAX_artist = int(x) -1
    def setMaxAlbum(self, x):
        self.MAX_album = int(x) -1
    def setMaxSong(self, x):
        self.MAX_song = int(x) -1

    def goDown(self):
        if self.column == 1:
            if self.artist < int(self.MAX_artist):
                self.artist += 1
        if self.column == 2:
            if self.album < int(self.MAX_album):
                self.album += 1
        if self.column == 3:
            if self.song < int(self.MAX_song):
                self.song += 1
    def goUp(self):
        if self.column == 1 :
            if self.artist > 0:
                self.artist -= 1
        if self.column == 2 :
            if self.album > 0:
                self.album -= 1
        if self.column == 3 :
            if self.song > 0:
                self.song -= 1
    def goLeft(self):
        if self.column == 3:
            self.song = 0
        if self.column == 2:
            self.album = 0
        if self.column > 1:
            self.column -= 1
        
    def goRight(self):
        if self.column < 3:
            self.column += 1
    def getCursor(self):
        return self
    def printCursor(self):
        print("Artist: "+str(self.artist)+ "\n Album: "+str(self.album) + "\n" +
              "Song: "+str(self.song) + "\n Column: " + str(self.column) + "\n \n \n" )
    def restartCursor(self):
        self.artist = 0
        self.album = 0
        self.song = 0
        self.column = 1

