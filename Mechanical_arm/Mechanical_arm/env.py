# -*- coding: utf-8 -*-
# @Author: Bin Liu
# @Date: 2018-06-18 14:25:58
# @Last Modified by: Bin Liu
# @Last Modified time: 2018-06-20 13:50:24
# @E-mail: monster910818@gmail.com or monster910818@163.com

import pyglet
import numpy as np


class ArmEnv(object):
    viewer = None
    dt = 0.1
    action_bound = [-1, 1]
    goal = {'x': 100., 'y': 100., 'l': 40}
    state_dim = 9
    action_dim = 2

    def __init__(self):
        self.arm_info = np.zeros(
            2, dtype=[('l', np.float32), ('r', np.float32)]
        )
        self.arm_info['l'] = 100
        self.arm_info['r'] = np.pi/6
        self.on_goal = 0

    def step(self, action):
        done = False
        action = np.clip(action, *self.action_bound)
        self.arm_info['r'] += action * self.dt
        self.arm_info['r'] %= np.pi * 2

        (a1l, a2l) = self.arm_info['l']
        (a1r, a2r) = self.arm_info['r']
        a1xy = np.array([200., 200.])
        a1xy_ = np.array([np.cos(a1r), np.sin(a1r)]) * a1l + a1xy
        finger = np.array([np.cos(a1r + a2r), np.sin(a1r + a2r)]) * a2l + a1xy_

        dist1 = [(self.goal['x'] - a1xy_[0] / 400, self.goal['y'] - a1xy_[1] / 400)]
        dist2 = [(self.goal['x'] - finger[0]) / 400, (self.goal['y'] - finger[1]) / 400]
        r = -np.sqrt(dist2[0] ** 2 + dist2[1] ** 2)


        if self.goal['x'] - self.goal['l'] / 2 < finger[0] < self.goal['x'] + self.goal['l']:
            if self.goal['y'] - self.goal['l'] / 2 < finger[1] < self.goal['y'] + self.goal['l']:
                r += 1.
                self.on_goal += 1
                if self.on_goal > 50:
                    done = True
        else:
            self.on_goal = 0
        s = np.concatenate((a1xy_ / 200, finger / 200, dist1 + dist2, [1. if self.goal else 0.]))
        return s, r, done


    def reset(self):
        self.arm_info['r'] = 2 * np.pi * np.random.rand(2)
        self.on_goal = 0
        (a1l, a2l) = self.arm_info['l']
        (a1r, a2r) = self.arm_info['r']
        a1xy = np.array([200., 200.])
        a1xy_ = np.array([np.cos(a1r), np.sin(a1r)]) * a1l + a1xy
        finger = np.array([np.cos(a1r + a2r), np.sin(a1r + a2r)]) * a2l + a1xy_
        dist1 = [(self.goal['x'] - a1xy_[0]) / 400, (self.goal['y'] - a1xy_[1]) / 400]
        dist2 = [(self.goal['x'] - finger[0]) / 400, (self.goal['y'] - finger[1]) / 400]
        s = np.concatenate((a1xy_ / 200, finger / 200, dist1 + dist2, [1. if self.on_goal else 0.]))
        return s

    def render(self):
        if self.viewer is None:
            self.viewer = Viewer(self.arm_info, self.goal)
        self.viewer.render()

    def sample_action(self):
        return np.random.rand(2) - 0.5


'''
定义可视化机械手臂，当不需要展示性能时，调用下面的函数
继承pyglet的窗口可视化模版
画出手臂
刷新手臂并呈现在屏幕上
刷新手臂的位置
更新手臂的位置信息
'''


class Viewer(pyglet.window.Window):
    bar_thc = 5

    def __init__(self, arm_info, goal):
        super(Viewer, self).__init__(width=400, height=400, resizable=False, caption='Arm', vsync=False)
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.arm_info = arm_info
        self.center_coord = np.array([200, 200])
        self.batch = pyglet.graphics.Batch()
        self.point = self.batch.add(4, pyglet.gl.GL_QUADS, None,
                                    ('v2f',
[goal['x'] - goal['l'] / 2, goal['y'] - goal['l'] / 2,
goal['x'] - goal['l'] / 2, goal['y'] + goal['l'] / 2,
goal['x'] + goal['l'] / 2, goal['y'] + goal['l'] / 2,
goal['x'] + goal['l'] / 2, goal['y'] - goal['l'] / 2]),
                                    ('c3B', [86, 109, 249] * 4))

        self.arm1 = self.batch.add(4, pyglet.gl.GL_QUADS, None,
                                    ('v2f', [250, 250,
                                             250, 300,
                                             260, 300,
                                             260, 250]),
                                    ('c3B', [249, 86, 86] * 4))
        self.arm2 = self.batch.add(4, pyglet.gl.GL_QUADS, None,
                                    ('v2f', [100, 150,
                                             100, 160,
                                             200, 160,
                                             200, 150]),
                                    ('c3B', [249, 109, 249] * 4))

    def render(self):
        self._update_arm()
        self.switch_to()
        self.dispatch_events()
        self.dispatch_event('on_draw')
        self.flip()

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def _update_arm(self):
        (a1l, a2l) = self.arm_info['l']
        (a1r, a2r) = self.arm_info['r']
        a1xy = self.center_coord
        a1xy_ = np.array([np.cos(a1r), np.sin(a1r)]) * a1l + a1xy
        a2xy_ = np.array([np.cos(a1r + a2r), np.sin(a1r + a2r)]) * a2l + a1xy_

        a1tr, a2tr = np.pi / 2 - self.arm_info['r'][0], np.pi / 2 - self.arm_info['r'].sum()
        xy01 = a1xy + np.array([-np.cos(a1tr), np.sin(a1tr)]) * self.bar_thc
        xy02 = a1xy + np.array([np.cos(a1tr), -np.sin(a1tr)]) * self.bar_thc
        xy11 = a1xy_ + np.array([np.cos(a1tr), -np.sin(a1tr)]) * self.bar_thc
        xy12 = a1xy_ + np.array([-np.cos(a1tr), np.sin(a1tr)]) * self.bar_thc

        xy11_ = a1xy_ + np.array([np.cos(a2tr), -np.sin(a2tr)]) * self.bar_thc
        xy12_ = a1xy_ + np.array([-np.cos(a2tr), np.sin(a2tr)]) * self.bar_thc
        xy21 = a2xy_ + np.array([-np.cos(a2tr), np.sin(a2tr)]) * self.bar_thc
        xy22 = a2xy_ + np.array([np.cos(a2tr), -np.sin(a2tr)]) * self.bar_thc

        self.arm1.vertices = np.concatenate((xy01, xy02, xy11, xy12))
        self.arm2.vertices = np.concatenate((xy11_, xy12_, xy21, xy22 ))

# 创建一个最终的视图主循环


if __name__ == '__main__':
    env = ArmEnv()
    while True:
        s = env.reset()
        for i in range(400):
            env.render()
            env.step(env.sample_action())
