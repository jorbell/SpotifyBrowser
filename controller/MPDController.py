#!/bin/env python
client = "x"
class MPDController:
    def connect(x):
        global client
        client = x
    def play():
        global client
        client.play()
    def pause():
        global client
        client.pause()
    def add(uri):
        global client
        client.add(uri)
    def playSongPos(pos):
        global client
        client.play(pos)
    def clear():
        global client
        client.clear()
