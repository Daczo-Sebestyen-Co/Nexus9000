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

def sin_osc(amplitude,transpose):                     # Sinus type generator
    sample = 0                                                      # The genarators own sample value
    for i in range(len(fr)):                                        # Goes through all the frequencies
        Fr = fr[i] * math.pow(step_ratio, transpose)                # Transposing the frequency
        value = amplitude * math.sin((s*2*math.pi)/(sample_rate/Fr))      # Calculating the current frequency value
        sample += value                                             # Adding the value
    return sample

def squ_osc(amplitude,transpose):                     # Square type generator
    sample = 0                                                    
    for i in range(len(fr)):                                    
        Fr = fr[i] * math.pow(step_ratio, transpose)               
        value = math.sin((s*2*math.pi)/(sample_rate/Fr))
        if value < 0:
            value = -1
        elif value > 0:
            value = 1
        else:
            value = 0
        sample += value * amplitude                                            
    return sample

def tri_osc(amplitude,transpose):                     # Sawtooth type generator
    sample = 0                                                    
    for i in range(len(fr)):                                    
        Fr = fr[i] * math.pow(step_ratio, transpose)               
        value = amplitude * (abs((s % (sample_rate/Fr))/(sample_rate/Fr)  * 2 - 1) * 2 - 1  )   
        sample += value                                             
    return sample

def saw_osc(amplitude,transpose):                     # Triangle type generator
    sample = 0                                                    
    for i in range(len(fr)):                                    
        Fr = fr[i] * math.pow(step_ratio, transpose)               
        value = amplitude * ((s % (sample_rate/Fr))/(sample_rate/Fr) * 2 -1)
        sample += value                                             
    return sample


def OSC(OSCs, Fr):
    global sample               # Holds the value of 1 piece of sample, which is beeing generated
    sample = 0
    global s                    # The numbre of sample, which is beeing generated
    s = 0
    global fr                   # The list of frequencies need to be played
    fr = Fr
    global sample_number        # How many samples are going to be generated
    simples = []                # Holding the samples in an array
    samples_number = sample_rate // 400 #math.lcm(fr) 
    samples = bytearray(samples_number * byte_res)  # This will hold the samples in byte array
    for s in range(samples_number):                 # Generating a sample
        for i in range(len(OSCs)):                  # Goes through the oscillators
            osc = OSCs[i]                           # The current oscillator
            wave_form = osc[0]                      # Checking the waveform
            if wave_form == 0 :
                sample += sin_osc(osc[1],osc[2])       # Adding the current OSCs value to the sample, based on the Frequencies and the transpose
            elif wave_form == 1 :
                sample += squ_osc(osc[1],osc[2])       # ---||---
            elif wave_form == 2 :
                sample += tri_osc(osc[1],osc[2])       # ---||---
            elif wave_form == 3 :
                sample += saw_osc(osc[1],osc[2])       # ---||---
        rangee = pow(2, bit_res) // 2                  # The range of the maximum sample value in the byte array
        sample = rangee + int((rangee - 1) * (sample/100))
        simples.append(int(sample))                 # Adding the sample to the array
        struct.pack_into("<h", samples, byte_res, sample)
        sample = 0                                  # Clear the sample value for the next round

    return samples    

