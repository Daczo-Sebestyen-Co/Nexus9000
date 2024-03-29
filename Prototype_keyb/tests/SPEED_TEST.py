# The MIT License (MIT)
# Copyright (c) 2022 Mike Teachman
# https://opensource.org/licenses/MIT

# Purpose:  Play a pure audio tone out of a speaker or headphones
#
# - write audio samples containing a pure tone to an I2S amplifier or DAC module
# - tone will play continuously in a loop until
#   a keyboard interrupt is detected or the board is reset
#
# Blocking version
# - the write() method blocks until the entire sample buffer is written to I2S

import os
import math
import struct
from machine import I2S
from machine import Pin
import time

# ======= I2S CONFIGURATION =======
SCK_PIN = 16
WS_PIN = 17
SD_PIN = 18
I2S_ID = 0
BUFFER_LENGTH_IN_BYTES = 2000
print("yes found it")
# ======= I2S CONFIGURATION =======


# ======= AUDIO CONFIGURATION =======
TONE_FREQUENCY_IN_HZ = 10000
SAMPLE_SIZE_IN_BITS = 16
FORMAT = I2S.MONO  # only MONO supported in this example
SAMPLE_RATE_IN_HZ = 48_000


sample_rate = SAMPLE_RATE_IN_HZ
step_ratio = math.pow(2, 1/12)


class makeOsc:
    class Sin:
        def __init__(self, amp, transpose, faze=0):
            self.amp = amp
            self.transpose = transpose
            self.faze = faze

        def getSample(self, s, fr_array):
            sample = 0                                                      # The genarators own sample value
            for i in range(len(fr_array)):                                        # Goes through all the frequencies
                Fr = fr_array[i] * math.pow(step_ratio, self.transpose)                # Transposing the frequency
                value = self.amp * math.sin(((s+self.faze)*2*math.pi)/(sample_rate/Fr))      # Calculating the current frequency value
                sample += value                                             # Adding the value
            return sample
    
    class Square:
        def __init__(self, amp, transpose, faze=0):
            self.amp = amp
            self.transpose = transpose
            self.faze = faze

        def getSample(self, s, fr_array):                     # Square type generator
            sample = 0                                                    
            for i in range(len(fr_array)):                                    
                Fr = fr_array[i] * math.pow(step_ratio, self.transpose)               
                value = math.sin(((s+self.faze)*2*math.pi)/(sample_rate/Fr))
                if value < 0:
                    value = -1
                elif value > 0:
                    value = 1
                else:
                    value = 0
                sample += value * self.amp                                            
            return sample

    class Triangle:
        def __init__(self, amp, transpose, faze=0):
            self.amp = amp
            self.transpose = transpose
            self.faze = faze

        def getSample(self, s, fr_array):                     # Sawtooth type generator
            sample = 0                                                    
            for i in range(len(fr_array)):                                    
                Fr = fr_array[i] * math.pow(step_ratio, self.transpose)               #transposing fr
                value = self.amp * (abs(((s+self.faze) % (sample_rate/Fr))/(sample_rate/Fr)  * 2 - 1) * 2 - 1  )   
                sample += value                                             
            return sample
        
    class Saw:
        def __init__(self, amp, transpose, faze=0):
            self.amp = amp
            self.transpose = transpose
            self.faze = faze

        def getSample(self, s, fr_array):                     # Triangle type generator
            sample = 0                                                    
            for i in range(len(fr_array)):                                    
                Fr = fr_array[i] * math.pow(step_ratio, self.transpose)               
                value = self.amp * (((s+self.faze) % (sample_rate/Fr))/(sample_rate/Fr) * 2 -1)
                sample += value                                             
            return sample

sawOSC = makeOsc.Saw(.3,0,0)
OSCs = [sawOSC]

def make_tone(rate, bits, frequency):
    # create a buffer containing the pure tone samples
    samples_per_cycle = rate // frequency
    sample_size_in_bytes = bits // 8
    samples = bytearray(samples_per_cycle * sample_size_in_bytes)
    volume_reduction_factor = 1
    range = pow(2, bits) // 2 // volume_reduction_factor
    
    if bits == 16:
        format = "<h"
    else:  # assume 32 bits
        format = "<l"
    
    sample = 0
    for i in range(samples_per_cycle):
        for osc in OSCs:
            sample += int((osc.getSample(i, [frequency]) * (range - 1) + (range/2))/ len(OSCs))
        struct.pack_into(format, samples, i * sample_size_in_bytes, sample)
        print(samples)
        
    return samples


# ======= AUDIO CONFIGURATION =======

audio_out = I2S(
    I2S_ID,
    sck=Pin(SCK_PIN),
    ws=Pin(WS_PIN),
    sd=Pin(SD_PIN),
    mode=I2S.TX,
    bits=SAMPLE_SIZE_IN_BITS,
    format=FORMAT,
    rate=SAMPLE_RATE_IN_HZ,
    ibuf=BUFFER_LENGTH_IN_BYTES,
)



# continuously write tone sample buffer to an I2S DAC
print("==========  START PLAYBACK ==========")
try:
    while True:
        t1 = time.ticks_cpu()
        samples = make_tone(SAMPLE_RATE_IN_HZ, SAMPLE_SIZE_IN_BITS, int(float(TONE_FREQUENCY_IN_HZ)))
        t2 = time.ticks_cpu()

        print(t1, t2, t2-t1)
        num_written = audio_out.write(samples)

except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))

# cleanup
audio_out.deinit()
print("Done")