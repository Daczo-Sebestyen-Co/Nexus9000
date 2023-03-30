from . import osc
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


osc.audio_setup(sample_rate, bit_res)
OSC0 = [0,100,0]
OSC1 = [0,0,0]
OSCs = [OSC0]
fr = [5000]
samples = osc.OSC(OSCs, fr)

print("==========  START PLAYBACK ==========")

try:
    while True:
        num_written = audio_out.write(samples)

except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))