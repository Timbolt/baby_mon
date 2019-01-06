import pyaudio
import wave
import audioop
import math


def play_wav():

    chunk = 1024

    # open the file for reading.
    wf = wave.open('rooster-36.wav', 'rb')

    # create an audio object
    p = pyaudio.PyAudio()

    # open stream based on the wave object which has been input.
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True,
                    output_device_index=3)

    # read data (based on the chunk size)
    data = wf.readframes(chunk)

    # play stream (looping from beginning of file to the end)
    while data != '':
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(chunk)

    # cleanup stuff.
    stream.close()
    p.terminate()

def runner():
    # See http://en.wikipedia.org/wiki/Bit_rate#Audio
    BITRATE = 16000  # number of frames per second/frameset.

    # See http://www.phy.mtu.edu/~suits/notefreqs.html
    FREQUENCY = 261.63  # Hz, waves per second, 261.63=C4-note.
    LENGTH = 1.2232  # seconds to play sound

    NUMBEROFFRAMES = int(BITRATE * LENGTH)
    RESTFRAMES = NUMBEROFFRAMES % BITRATE
    WAVEDATA = ''

    for x in range(NUMBEROFFRAMES):
        WAVEDATA += chr(int(math.sin(x / ((BITRATE / FREQUENCY) / math.pi)) * 127 + 128))

        # fill remainder of frameset with silence
    for x in range(RESTFRAMES):
        WAVEDATA += chr(128)

    p = pyaudio.PyAudio()
    stream = p.open(
        format=p.get_format_from_width(1),
        channels=1,
        rate=BITRATE,
        output=True,
        output_device_index=3
    )
    stream.write(WAVEDATA)
    stream.stop_stream()
    stream.close()
    p.terminate()


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 200
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            input_device_index=0)

xs = []
ys = []
x = 0
frames = []

exit_call = False

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):

    data = stream.read(CHUNK, exception_on_overflow=False)
    frames.append(data)
    rms = audioop.max(data, 2)    # here's where you calculate the volume

    x += 1
    ys.append(rms)
    xs.append(x)

    print(rms)

    if rms>1000:
        print(play_wav())

    f = open("guru99.txt", "a+")

    f.write(str(rms) + ',')


print(max(ys))

stream.stop_stream()
stream.close()
p.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(p.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()