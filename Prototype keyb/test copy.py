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

while True:
    button = [0,0,0]
    deactivate = [0,0,0]
    for row in rows:
        button[0] = rows.index(row)
        deactivate[0] = rows.index(row)
        makeNull(rows)
        row.value(1)
        for col in columns:
            if col.value():
                button[1] = columns.index(col)

                for lay in layers:
                    if lay.value():
                        button[2] = layers.index(lay)
                        if button not in pressed: pressed.append(button)
                        button = [0,0,0]
                    else:
                        deactivate[2] = layers.index(lay)
                        if deactivate in pressed:
                            pressed.pop(pressed.index(deactivate))
                            deactivate = [0,0,0]
            else:
                for lay in layers:
                    deactivate[1] = columns.index(col)
                    deactivate[2] = layers.index(lay)
                    if deactivate in pressed:
                        pressed.pop(pressed.index(deactivate))
                        deactivate = [0,0,0]
            
        print(pressed)




