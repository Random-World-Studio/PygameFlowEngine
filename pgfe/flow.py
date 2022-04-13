"""
flow.py
Flow类是流引擎的核心类，
它真正运行了窗口的刷新流
"""

import pygame as pg
import threading

from evehandle import EveHandle
from efont import create_font


def defaultFlash() -> bool:
    pg.display.flip()
    return True


class Flow:  # 刷新流类

    # 状态常量
    UNINIT = 0
    RUNNING = 1
    STOP = 2
    DEAD = 3

    fpsdelay = pg.time.Clock()

    tpf = 0  # tick per frame
    real_fps = 0  # 实际帧率

    fps_visi = False

    def __init__(self, screen: pg.Surface,  # 流运行的表面
                 bgcolor=(0, 0, 0),  # 背景颜色
                 flash=defaultFlash,  # 绘图函数
                 fps: int = 60,  # 期望帧率
                 exitfunc=exit,  # 退出函数
                 *evelist: EveHandle  # 关注的事件列表
                 ):
        self.screen = screen
        self.bgColor = bgcolor
        self.flash = flash
        self.fps = fps
        self.exitfunc = exitfunc
        self.state = self.UNINIT
        self.evelist = evelist
        self.flow_thread = threading.Thread(target=self.run)
        self.fps_visi = False

    def run(self):
        tick = 0
        flowterm = True
        while self.state != self.DEAD and flowterm is True:  # 流未处于DEAD状态，并且刷新函数没有返回False
            # 计算帧率
            last_tick = tick
            tick = pg.time.get_ticks()
            self.tpf = tick - last_tick
            self.real_fps = 1000 / self.tpf
            # 刷新屏幕
            pg.display.flip()
            self.fpsdelay.tick(self.fps)
            # 首先检测是否处于STOP状态
            if self.state == self.STOP:
                continue
            # 接收事件
            for event in pg.event.get():
                if event.type == pg.QUIT:  # 先拦截QUIT事件
                    self.exitfunc(0)
                    exit(0)  # 防止exitfunc最后不调用exit(0)
                for __event in self.evelist:  # 遍历关注事件列表
                    if __event.getType() == event.type:
                        __event.getHandler()()  # 执行事件handler
            self.screen.fill(self.bgColor)  # 清屏
            flowterm = self.flash()  # 绘制
            if self.fps_visi:  # 显示帧率
                self.screen.blit(create_font('fps: {}'.format('%f.2' % self.fps)), (0, 0))

    def get_fps(self):  # 获取帧率
        return self.fps

    def set_fps_visible(self, visible: bool):  # 是否显示帧率
        self.fps_visi = visible

    def start(self):  # 开启刷新流
        if self.state == self.UNINIT:
            self.state = self.RUNNING
            self.flow_thread.start()
        elif self.state == self.STOP:
            self.state = self.RUNNING

    def stop(self):  # 暂停刷新流
        self.state = self.STOP

    def kill(self):  # 终止刷新流
        self.state = self.DEAD
