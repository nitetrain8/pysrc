"""

Created by: Nathan Starkweather
Created on: 02/12/2014
Created in: PyCharm Community Edition


"""

    x = 111213123
    y = x
    print(y is x)

    for x in range(1000000, 10000000):
        y = x
        if not y is x:
            print(x)

    m = [1, 2, 3, 4, 5]
    n = m
    print(m is n)
    m = [1, 2, 3]
    print(n)
    print(n is m)
