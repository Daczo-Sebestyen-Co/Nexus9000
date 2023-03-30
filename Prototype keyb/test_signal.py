import machine
import time

rows = [machine.Pin(4, machine.Pin.OUT), machine.Pin(5, machine.Pin.OUT)]
columns = [machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_DOWN), machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_DOWN), machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_DOWN)]
layers = [machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_DOWN), machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_DOWN), machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_DOWN)]



def makeNull(l):
    for e in l:
        e.value(0)

pressed = []
c = []
l = []

rows[0].value(1)
rows[1].value(1)
while True:
    for r in rows:
        print(r.value(), end=" ")
    print("", end=" ")
    for c in columns:
        print(c.value(), end=" ")
    print("", end=" ")
    for l in layers:
        print(l.value(), end=" ")
    print("")


