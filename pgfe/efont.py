import pygame as pg


def create_font(string: str, size: int = 20, font: str = pg.font.get_fonts()[0], color=None) -> pg.Surface:
    if color is None:
        color = [255, 255, 255]
    fnt = pg.font.SysFont(font, size)
    fnt.render(string, True, color)
    return fnt
