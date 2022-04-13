import pygame as pg


class EveHandle:
    def __init__(self, event_t, handler):
        self.event_t = event_t
        self.handler = handler

    def getType(self):
        return self.event_t

    def getHandler(self):
        return self.handler
