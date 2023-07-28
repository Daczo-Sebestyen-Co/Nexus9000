import os
import math
import struct
from machine import I2S
from machine import Pin
import _thread
import theSignal

# ======= I2S CONFIGURATION =======
SCK_PIN = 16
WS_PIN = 17
SD_PIN = 18
I2S_ID = 0
BUFFER_LENGTH_IN_BYTES = 2000
print("yes found it")
# ======= I2S CONFIGURATION =======


# ======= AUDIO CONFIGURATION =======
TONE_FREQUENCY_IN_HZ = 440
SAMPLE_SIZE_IN_BITS = 16
FORMAT = I2S.MONO  # only MONO supported in this example
SAMPLE_RATE_IN_HZ = 60_000

sample_rate = SAMPLE_RATE_IN_HZ
step_ratio = math.pow(2, 1/12)

class makeOsc:
    class Sin:
        def __init__(self, amp : float, transpose, faze=0):
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
        def __init__(self, amp : float, transpose, faze=0):
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
        def __init__(self, amp : float, transpose, faze=0):
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
        def __init__(self, amp : float, transpose, faze=0):
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

#tri_osc = makeOsc.Triangle(.1, 0, 0)
#sin_osc = makeOsc.Sin(1,0,1)
#sin_osc2 = makeOsc.Sin(1,0,0)
saw_osc = makeOsc.Saw(.4,0,0)
#squ_osc = makeOsc.Square(1,0,0)
OSCs = [saw_osc]

startamp = saw_osc.amp

attack = 1
decay = .5
release = 0

isAttack, isDecay, isRelease = True, False, False
attackSpeed, decaySpeed, releaseSpeed = 1/sample_rate * 20, -1/sample_rate * 5, -1/sample_rate * 10

def make_tone(rate, bits, frequency):
    global isAttack, isDecay, isRelease
    # create a buffer containing the pure tone samples
    samples_per_cycle = rate // frequency * 1 #!!!!!!!!!!!
    sample_size_in_bytes = bits // 8
    samples = bytearray(samples_per_cycle * sample_size_in_bytes)
    volume_reduction_factor = 1.5
    range = pow(2, bits) // 2 // volume_reduction_factor
    sample = 0
    
    if bits == 16:
        format = "<h"
    else:  # assume 32 bits
        format = "<l"
    
    lastfreq = None
    for i in range(samples_per_cycle):
        for osc in OSCs:
            sample += int((osc.getSample(i, [frequency]) * (range - 1) + (range/2))/ len(OSCs))
            print(osc.amp, isAttack, isDecay, isRelease)

            if isAttack:
                if osc.amp < attack:
                    osc.amp += attackSpeed
                else:
                    isAttack = False
                    isDecay = True

            if isDecay:
                if osc.amp > decay:
                    osc.amp += decaySpeed
                else:
                    isDecay = False
                    isRelease = True

            if frequency != lastfreq:
                if lastfreq != None:
                    isDecay = False
                    isRelease = True

            if isRelease:
                if osc.amp > 0:
                    osc.amp += releaseSpeed
                else:
                    osc.amp = 0
            
                    if lastfreq != frequency:
                        isAttack = True
                        isRelease = False
                
            lastfreq = frequency
            
        #
        #int(range / 2 + (range - 1) * math.sin(2 * math.pi * i / samples_per_cycle))
        struct.pack_into(format, samples, i * sample_size_in_bytes, sample)
        sample = 0
        #print(samples)
        
        
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

samples = None
def write_Samples():
    global samples
    while True:
        try:
            if samples != None and type(samples) == bytearray:
                audio_out.write(samples)
        except (Exception, KeyboardInterrupt) as e:
            print(e, samples, "_____________________________________")


def startMain():
    global samples
    try:
        while True:
            s = theSignal.getFreq() #e: 440 erre átalakítani: [440, 1 (amp)]
            #s = 8100 #!!!!!
            #print(isAttack, isDecay, isRelease, s, lastfreq)
            
            #print(s, type(s))
            if s != None:
                import time
                t1 = time.ticks_cpu()
                samples = make_tone(SAMPLE_RATE_IN_HZ, SAMPLE_SIZE_IN_BITS, int(float(s)))
                t2 = time.ticks_cpu()
                #print(t1, t2, t2-t1)
                #num_written = audio_out.write(samples)
            #else: !!!!!!!!!!!!!!!!!!!!!
                #samples = None
                    
    except KeyboardInterrupt as e:
        print("KEYBOARD INTERRUPTION")
        #_thread.exit()

t1 = _thread.start_new_thread(write_Samples, ())
startMain()

# cleanup
audio_out.deinit()
print("Done")


