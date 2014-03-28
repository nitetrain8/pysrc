"""

Created by: Nathan Starkweather
Created on: 03/27/2014
Created in: PyCharm Community Edition


"""
__author__ = 'Nathan Starkweather'
from decimal import Decimal as D


def _fudge(i, x_prev, y_prev, ydiff_over_tdiff):
    return (i - x_prev) * ydiff_over_tdiff + y_prev


def smooth1(xd, yd):

    decimal = D

    xd = tuple(map(round, xd))
    yd = tuple(map(decimal, yd))

    x_prev = xd[0]
    x_end = xd[-1]
    y_start = y_prev = yd[0]

    y_data = [y_start] * (x_end + 1)

    data = zip(xd, yd)
    next(data)
    fudge = _fudge

    for x_next, y_next in data:

        i = x_prev
        ydiff_over_tdiff = (y_next - y_prev) / decimal(x_next - x_prev)

        while i < x_next:
            i += 1
            y_data[i] = fudge(i, x_prev, y_prev, ydiff_over_tdiff)

        x_prev = x_next
        y_prev = y_next

    x_data = list(range(len(y_data)))

    return x_data, y_data
