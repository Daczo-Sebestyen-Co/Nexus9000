# =====/// NEXUS ///=====
# This code is owned by the Great and Nobel company of FaireFox™

import struct
import math
from machine import I2S, Pin


# I2S Pins
pcm_bck = 16
pcm_lrc = 17
pcm_din = 18
# I2S Settings
pcm_id = 0
bit_res = 16
sample_rate = 44100
bif_buf = 2000
form = I2S.MONO

buf_form = "<h"


audio_out = I2S(pcm_id,sck=Pin(pcm_bck),ws=Pin(pcm_lrc),sd=Pin(pcm_din),mode=I2S.TX,bits=bit_res,format=form,rate=sample_rate,ibuf=bif_buf,)


# ---Sample stuff---
def sin_osc(freq, amplitude):
    sample_points = sample_rate // freq
    sample_bytes = bit_res // 8
    samples = bytearray(sample_points * sample_bytes)
    value_range = pow(2, bit_res) // 2 // (64*8) 

    for i in range(sample_points):
        org = (value_range - 1) * math.sin((i * 2 * math.pi)/sample_points)
        sec = (value_range - 1) * math.sin((i * 4 * math.pi)/sample_points)
        thi = (value_range - 1) * math.sin((i * 8 * math.pi)/sample_points)
        sample_value = int(org + sec + thi) + value_range
        
        struct.pack_into(buf_form, samples, i * sample_bytes, sample_value)
        #print(i, "\t", sample_value, "\t", samples[i*2-2], "\t", samples[i*2-1])
    
    return samples
def squ_osc(freq, amplitude):
    sample_points = sample_rate // freq
    sample_bytes = bit_res // 8
    samples = bytearray(sample_points * sample_bytes)
    value_range = pow(2, bit_res) // 32

    for i in range(sample_points):
        sample_value = int((value_range - 1) * math.sin((i * 2 * math.pi)/sample_points))
        if sample_value > 0:
            sample_value = value_range-1
        else:
            sample_value = 0
        struct.pack_into(buf_form, samples, i * sample_bytes, sample_value)
        #print(i, "\t", sample_value, "\t", samples[i*2-2], "\t", samples[i*2-1])
    
    return samples


buffer = sin_osc(440, 1)

print("____STARTED____")
try:
    while True:
        num_written = audio_out.write(buffer)

except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))

audio_out.deinit()
print("Done")

# Copyrigt | all rights reserved | 2022