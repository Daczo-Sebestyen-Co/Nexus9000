import math
import struct

sample_rate = 0
bit_res = 0
byte_res = 0
step_ratio = math.pow(2, 1/12)



def audio_setup(Sample_rate, Bit_res):
    global sample_rate
    global bit_res
    global byte_res
    sample_rate, bit_res = Sample_rate, Bit_res
    byte_res = Bit_res // 8

# osc1 wave_form = 0, ampitude = 0.3, transpose = 24

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
                Fr = fr_array[i] * math.pow(step_ratio, self.transpose)               
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

def OSC(OSCs, fr_array):
    sample = 0
    global sample_number        # How many samples are going to be generated
    samples_array = []                # Holding the samples in an array
    samples_number = sample_rate // 5000 #math.lcm(fr_array) 
    samples = bytearray(samples_number * byte_res)  # This will hold the samples in byte array
    for s in range(samples_number):                 # Generating a sample
        for osc in OSCs:                  # Goes through the oscillators
            sample += osc.getSample(s, fr_array) / len(OSCs)

        samples_array.append(int(sample))              # Adding the sample to the array
        struct.pack_into("<h", samples, byte_res, int(sample))
        sample = 0                                  # Clear the sample value for the next round

    return samples_array #samples to make bytearray!!!

#----------test----------

if __name__ == "__main__":
    audio_setup(40000, 2000)
    sin = makeOsc.Sin(10, 0, 0)
    squ2 = makeOsc.Square(10, 0, 1)
    print(OSC([squ2], [5000]))
    print(OSC([squ2, sin], [5000]))
