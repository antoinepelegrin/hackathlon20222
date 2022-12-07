import pyaudio
import wave
import whisper

from pydub import AudioSegment

"""
Script records audio from mic for five (variable) seconds, saves in *.wav format and then run a Whisper pre-trained model 
to transcribe the audio to text.
"""

# Variables
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "audio.wav"

p = pyaudio.PyAudio()

frames = []

stream = p.open(format = FORMAT,
                channels = CHANNELS, 
                rate = RATE, 
                input = True,
                frames_per_buffer = CHUNK)

print("Recording...")
for i in range(0 , int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("Done recording...")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# Load Whisper model for transcribing audio file
model = whisper.load_model("tiny")
print("Transcribing audio file...")
result = model.transcribe("audio.wav")
print("Output is \n:")
print(result["text"])