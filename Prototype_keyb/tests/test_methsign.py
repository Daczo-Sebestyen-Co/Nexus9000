import machine
import time

rows = [machine.Pin(4, machine.Pin.OUT), machine.Pin(5, machine.Pin.OUT)]
columns = [machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_DOWN), machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_DOWN), machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_DOWN)]
layers = [machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_DOWN), machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_DOWN), machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_DOWN)]


def makeNull(l):
    for e in l:
        e.value(0)

while True:
    pressed = []
    button = [0,0,0]
    for row in rows:
        button[0] = rows.index(row)
        makeNull(rows)
        row.value(1)
        for col in columns:
            if col.value():
                for lay in layers:
                    if lay.value():
                        print(button[0], col, lay)
