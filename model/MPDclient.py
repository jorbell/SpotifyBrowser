#!/bin/env python
from mpd import MPDClient
client = "x"
def connect():
    global client
    client = MPDClient()               # create client object
    client.timeout = 10                # network timeout in seconds (floats allowed), default: None
    client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
    client.connect("localhost", 6666)  # connect to localhost:6600
    return client;

def add(uri):
    global client
    client.add(uri)
def pause():
    global client
    client.pause(1)
def play():
    global client
    client.pause(0)
