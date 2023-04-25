# not for the Pico
import math

def get_sine(sample_rate, amplitude, frequency):
    samples_N = sample_rate // frequency
    #samples = [math.sin(i) for i in range(int(samples_N))]
    samples = []
    for i in range(int(samples_N)):
        steps = (2 * math.pi * i) / samples_N
        steps = int(100 * math.sin(steps))
        samples.append(steps)
        print(i, "\t", samples[i], "\t", )
    print(samples)

get_sine(512, 1, 16)
