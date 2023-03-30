import math

class makeOsc:
    def __init__(self, ampl, t, fr, sample_rate):
        self.step_ratio = math.pow(2, 1/12)

        self.t = t
        self.fr = fr
        self.sample_rate = sample_rate

    def osc(self, s):                     # Sinus type generator
        sample = 0                                                      # The genarators own sample value
        for i in range(len(self.fr)):                                        # Goes through all the frequencies
            Fr = self.fr[i] * math.pow(self.step_ratio, self.t)                # Transposing the frequency
            value = 100 * math.sin((s*2*math.pi)/(self.sample_rate/Fr))      # Calculating the current frequency value
            sample += value                                             # Adding the value
        return sample

sinOsc = makeOsc(0, 0, [5000], 40000)

print(int(sinOsc.osc(2)))

