from tkinter import *
from functools import partial
from logger import *

# logger.info("hi")

def a(x, y):
    print(x + y)


window = Tk()
# d = Button(window, text="b", command=partial(a, 1, 2))
e = Entry(window)
e.grid(column="0")
print(e.get)
d = Button(window, text="b", command=lambda: a(1,2))
d.grid(column="1")

window.mainloop()

# ++++++++++++++++

# def a (x=1, y=2):
#     print(x+y)
#
#
# d = {"x": 3, "y": 4}
# # d = {}
# a(**d)
