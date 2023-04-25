import matplotlib.pyplot as plt
import math

x = []
y = []
for i in range(1,100):
    #iks = (i**(-1)**i+1)*(math.sin(i)/i) #int(i**(-1)**i+1)
    samplr = 40000
    apmpl = 1
    frq = 2000
    maxi = 0
    period = samplr/frq

    iks = (i % period)/period * 2 -1

    print(period)

for i in range(1,100):
    #iks = (i**(-1)**i+1)*(math.sin(i)/i) #int(i**(-1)**i+1)
    samplr = 40000
    apmpl = 1
    frq = 2000
    maxi = 0
    period = samplr/frq

    iks = abs((i % period)/period  * 2 - 1) * 2 - 1

    print(period)

    
    y.append(iks)
    x.append(i)
    print(iks)

plt.bar(x, y)
plt.title('title name')
plt.xlabel('x_axis name')
plt.ylabel('y_axis name')
plt.show()
