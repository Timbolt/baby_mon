import wave
import pyaudio
import time

def play_wav(wait_time, loud=False):

    chunk = 1024

    # open the file for reading.
    if loud:
        wf = wave.open('/home/pi/Desktop/baby_mon/rooster-15.wav', 'rb')
    else:
        wf = wave.open('/home/pi/Desktop/baby_mon/rooster-36.wav', 'rb')

    # create an audio object
    p = pyaudio.PyAudio()

    # open stream based on the wave object which has been input.
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True,
                    output_device_index=0)

    # read data (based on the chunk size)
    data = wf.readframes(chunk)

    start_time = time.time()
    current_time = start_time

    # play stream (looping from beginning of file to the end)
    while current_time-start_time < min(wait_time, 5): # need to be no more than wait_time otherwise it triggers itself all the time
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(chunk)

        current_time = time.time()

    # cleanup stuff.
    stream.close()
    p.terminate()