import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id='9e638d6be17e4fb8afe62d1cab43d16e'
client_secret='30990f5f6f90429dbdef5b928bcb1bd9'
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class Artist: 
    name=""
    id=""
    albums=[]
    uri=""
    followers=""
    relatedArtists=[]
    genres=[]

class Album:
    name=""
    type=""
    uri=""
    albumID=""
    artistID=""
    artistName=""
    songs=[]

class Song:
    name=""
    artist=""
    album=""
    uri=""
def getRelatedArtists(arObj):
    #r = sp.get_artist(arObj['id'])
    r = sp.artist_related_artists(arObj.id)
    ra=[]
    for artist in r['artists']:
        tmp = Artist()
        tmp.name = artist['name']
        tmp.id = artist['id']
        tmp.uri = artist['uri']
        ra.append(tmp)
    arObj.relatedArtists=ra

    return arObj

def searchArtist(artist):
    #results = sp.search(q='artist:' + artist, type='artist')
    results = sp.search(q='artist:' + artist, type='artist')
    artists = []
    for item in results['artists']['items']:
        arObj = Artist()
        arObj.name = item['name']
        arObj.id = item['id']
        arObj.followers = item['followers']['total']
        albums = getArtistAlbums(item['id'])['items']
        #arObj = getRelatedArtists(arObj)
        for genre in item['genres']:
            arObj.genres.append(genre)
        artists.append(arObj)
        


    #print(results['artists']['items'][0])
    return artists

def searchAlbum(album):
    results = sp.search(q='album:' + album, type='album')

    albums = []
    for item in results['albums']['items']:
        alObj = Album()
        alObj.name=item['name']
        alObj.type=item['album_type']
        alObj.uri=item['uri']
        alObj.artistID=item['artists'][0]['id']
        artistID=item['artists'][0]['id']
        alObj.artistname=getArtistName(artistID)
        albums.append(alObj)
    return albums

def setArtistAlbums(artist):
        albums = getArtistAlbums(artist.id)['items']
        for album in albums:
            alObj = Album()
            alObj.artistName = artist.name
            alObj.artistID = artist.id
            alObj.name=album['name']
            alObj.type=album['album_type']
            alObj.uri=album['uri']
            alObj.albumID=album['id']
            artist.albums.append(alObj)
        return artist

def setAlbumSongs(album):
        songs = getAlbumSongs(album.albumID)['items']
        #songs = [1,2,3,4,5,6,7]
        for song in songs:
            songObj = Song()
            songObj.name = song['name'] 
            songObj.artistID = album.artistID;
            songObj.album = album;
            songObj.uri = song['uri']
            album.songs.append(songObj);
        return album
def searchSong(song):
    result = sp.search(q='track:' + song, type='track')
    return result
def getArtistAlbums(artistID):
    albums = sp.artist_albums(artistID)
    return albums
def getAlbumSongs(albumID):
    songs = sp.album_tracks(albumID)
    return songs
def getArtistName(artistID):
    artistname = sp.artist(artistID)['name']
    return artistname
