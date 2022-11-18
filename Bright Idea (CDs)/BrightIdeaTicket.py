# BrightIdeaTicket.py

class BrightIdeaTicket:
    def __init__(self, imgs, tier, eyed=''):
        self._images = imgs
        self._tier = tier
        self._id = eyed
        self._up = ''
        self._sheet = ''
        self._position = ''

    def images(self, i=None):
        if i: self._images = i
        return self._images

    def tier(self, t=None):
        if t: self._tier = t
        return self._tier

    def id(self, i=None):
        if i: self._id = i
        return self._id

    def up(self, u=None):
        if u: self._up = u
        return self._up

    def sheet(self, s=None):
        if s: self._sheet = s
        return self._sheet

    def position(self, p=None):
        if p: self._position = p
        return self._position
