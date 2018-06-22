# -*- coding: utf-8 -*-
# @Author: Bin Liu
# @Date: 2018-06-18 14:32:27
# @Last Modified by: Bin Liu
# @Last Modified time: 2018-06-20 13:51:51
# @E-mail: monster910818@gmail.com or monster910818@163.com

# 导入环境和学习方法

from .env import ArmEnv
from Mechanical_arm.rl import DDPG

# 设置全局变量
MAX_EPISODES = 500
MAX_EP_STEPS = 200
ON_TRAIN = True

'''
设置环境
s_dim = 多少个状态
a_dim = 多少个动作
a_bound= 输出范围
'''
env = ArmEnv()
s_dim = env.state_dim
a_dim = env.action_dim
a_bound = env.action_bound

# 引用RL的训练方法
rl = DDPG(s_dim, a_dim, a_bound)

'''
开始训练
在最大回合循环中，设置一个初始值 s
在最大步数中，返回可视化的函数
通过神经网络的输入的初始化值，得出一个输出值机械手臂的动作 a
再将a的环境反馈给出输入下一个 s_，重述步骤 r，与结束 done
在强化学习中，可以将上述参数放入离线记忆库中强化学习
'''

steps = []


def train():
    for i in range(MAX_EPISODES):
        s = env.reset()
        for j in range(MAX_EP_STEPS):
            env.render()

            a = rl.choose_action(s)

            s_, r, done = env.step(a)

            rl.store_trainsition(s, a, r, s_)

            ep_r += r

            if rl.memory_full():
                rl.learn()

            s = s_
            if done or j == MAX_EP_STEPS-1:
                print('Ep: %i | %s | ep_r: %.1f | step: %i' % (i, '---' if not done else 'done', ep_r, j))
                break
    rl.save()


def eval():
    rl.restore()
    env.render()
    env.viewer.set_vsync(True)
    while True:
        s = env.reset()
        for _ in range(200):
            env.render()
            a = rl.choose_action(s)
            s, r, done = env.step(a)
            if done:
                break


if ON_TRAIN:
    train()
else:
    eval()
