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
    for row in rows:
        makeNull(rows)
        row.value(1)
        for col in columns:
            #print(col)
            if col.value():
                c.append(f"{rows.index(row)} {columns.index(col)}")
                
            else:
                try:
                    c.pop(columns.index(col))
                except:
                    pass
            for lay in layers:
                    if lay.value():
                        l.append(f"{rows.index(row)} {layers.index(lay)}")
                    else:
                        try:
                            l.pop(layers.index(lay))
                        except:
                            pass
        print(c, l)


"""rows[].value(1)
row1.value(1)
while True:
    print(row0.value(), row1.value(), column0.value(), column1.value(), column2.value(), layer0.value(), layer1.value(), layer2.value())
"""

