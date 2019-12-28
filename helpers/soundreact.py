import pyaudio
import numpy as np
from time import time

CHUNK = 4096 # number of data points to read at a time
#RATE = 44100 # time resolution of the recording device (Hz)
#RATE = 11025
RATE = 48000


from pythonosc import osc_message_builder
from pythonosc import udp_client


sendToAddress           = "127.0.0.1"
sendToPort              = 5433
oscName                 = "/volume"

threshold = 0.5
last_triggered = time()
threshold_time = 1
threshold_limit = 5 
threshold_count = 0

client = udp_client.SimpleUDPClient(sendToAddress, sendToPort)


p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                      frames_per_buffer=CHUNK) #uses default input device

# create a numpy array holding a single read of audio data
#for i in range(10): #to it a few times just to see
i = 0
while True:
        i += 1
        data = np.fromstring(stream.read(CHUNK, exception_on_overflow = False),dtype=np.int16)
        print(data)
        peak=np.average(np.abs(data))*2
        bars="#"*int(50*peak/2**16)
        print("i:%04d peak:%05d bars:%s"%(i,peak,bars))

        value = peak/32768.0

        if value > threshold:
            print("triggered count is %s"% threshold_count)
            last_triggered = time()
            threshold_count += 1

        if threshold_count > threshold_limit:
            print("been triggered too many times - drop threshold")
            threshold = value
            threshold_count = 0

        if time()-last_triggered > threshold_time:
            print("%s + %s > %s" % (last_triggered,threshold_time,time()))
            print("too long since triggered, drop threshold")
            threshold = value
        else:
            print("%s + %s > %s" % (last_triggered,threshold_time,time()))

        #mod = 1/threshold
        #value *= mod

        print("sending %s (current threshold is %s)" % (value, threshold))
        client.send_message(oscName, value) #random.random())

        # close the stream gracefully
stream.stop_stream()
stream.close()
p.terminate()
