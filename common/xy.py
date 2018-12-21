#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/12/17 18:58    @Author  : xycfree
# @Descript: 

def xy(x, y):
    if (3*x + 2*y) == 50 and 150 * x + 140 * y == 1510 *2 :
        print("答案: 三人间：{},二人间: {}".format(x, y))
    else:
        pass

if __name__ == '__main__':
    for i in range(50):
        for j in range(50):
            xy(i, j)
    print('end')


