#!/bin/env python
spot = "x"
class SpotifyController:
    def setSpotify(x):
        global spot
        spot = x
    def searchAlbum(album):
        return spot.searchAlbum(album)
    def searchArtist(artist):
        return spot.searchArtist(artist)
    def searchSong(song):
        return spot.searchSong(song)
    def getArtistAlbums(artistID):
        return spot.getArtistAlbums(artistID)
    def getArtistName(artistID):
        return spot.getArtistName(artistID)
    def setArtistAlbums(artist):
        return spot.setArtistAlbums(artist)
    def setAlbumSongs(album):
        return spot.setAlbumSongs(album)
    def getRelatedArtists(artist):
        return spot.getRelatedArtists(artist)
