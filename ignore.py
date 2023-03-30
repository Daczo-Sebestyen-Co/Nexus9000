class makeOsc:
    class makeSin:
        def __init__(self, x, amp):
            self.x = x
            self.amp = amp

o = makeOsc.makeSin(10, 1)
print(o.x)
