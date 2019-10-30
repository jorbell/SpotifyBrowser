#!/bin/env python
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from mpd import MPDClient

class Artist: 
    name=""
    id=""
    albums=[]
    uri=""
    def printAlbums(self):
        i = 0
        for album in self.albums:
            print("\t  "+ str(i) +" " +album.type + ": " + album.name)
            i += 1
class Album:
    name=""
    type=""
    uri=""


def connectMPD():
    client = MPDClient()               # create client object
    client.timeout = 10                # network timeout in seconds (floats allowed), default: None
    client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
    client.connect("localhost", 6666)  # connect to localhost:6600

    return client;

def addToPlaylist(uri):
    client.add(uri)


def searchArtist(artist):
    #results = sp.search(q='artist:' + artist, type='artist')
    results = sp.search(q='artist:' + artist, type='artist')
    artists = []
    i = 0
    for item in results['artists']['items']:
        arObj = Artist()
        arObj.name = item['name']
        #print(item['name'])
        print(arObj.name)
        #print(item['id']) 
        albums = getArtistAlbums(item['id'])['items']
        for album in albums:
            alObj = Album()
            alObj.name=album['name']
            alObj.type=album['album_type']
            alObj.uri=album['uri']
            #print("\t" + album['album_type'] + ": " + album['name'])
            arObj.albums.append(alObj)
            #print(arObj.albums[0].name)
        arObj.printAlbums()
        artists.append(arObj)

    return artists

def searchAlbum(album):
    results = sp.search(q='album:' + album, type='album')
    #print(results['albums']['items'])
    for item in results['albums']['items']:
        name = item['name']
        #print(item['name'])
        addToPlaylist(item['uri'])
        artistID=item['artists'][0]['id']
        artistname=getArtistName(artistID)
        #print(artistID)
        #artist=str(item['artists'][0]['id'])
        #artist=getArtistName(item['artists'][0]['id'])
        print("Album name: " + name + "    Artist: "+artistname)
        #print(name)
        #print(artistname)
def getArtistAlbums(artistID):
    albums = sp.artist_albums(artistID)
    return albums

def getArtistName(artistID):
    #sp.artist(artistID)
    #print(sp.artist(artistID)['name'])
    #return sp.artist(artistID['name'])
    artistname = sp.artist(artistID)['name']
    return artistname




#MPD client
client = connectMPD()
##Spotify client definitions
client_id='9e638d6be17e4fb8afe62d1cab43d16e'
client_secret='30990f5f6f90429dbdef5b928bcb1bd9'
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)




#addToPlaylist(results['albums']['items'][0]['artists'][0]['uri'])

#searchArtist("cmx")
#searchAlbum("mooncake")
i = 2
search = " "
ask = True
while i < len(sys.argv):
    if sys.argv[i] == "-l":
        ask = False

    else:
        search += sys.argv[i] + " "
    i += 1
#print(search)
    
if sys.argv[1] == "-al":
    results = searchAlbum(search)
if sys.argv[1] == "-ar":
    results = searchArtist(search)
i = 0;
j = 0;
for artist in results:
    print("MAIN FOR LOOP")
    print(str(i) + artist.name)
    artist.printAlbums()
    i += 1
    #print(artist.albums[0].uri)
#addToPlaylist(results[0].albums[0].uri)
if ask == True:
    arnr = int(input("Give artist number: "))
    alnr = int(input("Give album number: "))
    i = 0
    j = 0
    for artist in results:
        if i == arnr:
            for album in artist.albums:
                if j == alnr:
                    addToPlaylist(album.uri)
                j += 1
        i+=1



