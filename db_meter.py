import pyaudio
import wave
import audioop
import datetime, time
import wave_player
import speech_recognition as sr

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 20
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            input_device_index=0)


frames = []

exit_call = False
start_time = time.time()

max_v_list = []

new_run = True

small_trigger = 0

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):

    data = stream.read(CHUNK, exception_on_overflow=False)
    frames.append(data)
    max_v = audioop.max(data, 2)    # here's where you calculate the volume
    max_v_list.append(max_v)
    print(max_v)


    wait_time = 6

    # large trigger
    if len(max_v_list) > 20: # make sure list is long enough
        if max(max_v_list[-200:-1]) >= 1500 and small_trigger > 3: # if small trigger triggered 4+ times AND there was a loud noise recently
            current_time = time.time()
            if current_time - start_time > wait_time:
                wave_player.play_wav(wait_time, loud=True)
                start_time = time.time()

    # small trigger
    if max_v>100 and max_v <1500:
        current_time = time.time()
        if current_time - start_time > wait_time:
            wave_player.play_wav(wait_time)
            start_time = time.time()
            small_trigger += 1

    if new_run:
        time_id = datetime.datetime.now()
        f = open("sound_tracking/st_{}.csv".format(time_id), "w")
        f.write('sound_level, date, time \n')
        new_run = False
    else:
        f = open("sound_tracking/st_{}.csv".format(time_id), "a+")
        f.write('{},{},{} \n'.format(str(max_v), str(datetime.datetime.now().date()), str(datetime.datetime.now().time())))


stream.stop_stream()
stream.close()
p.terminate()
