import argparse
import io
import os
import speech_recognition as sr
import whisper

from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep

from browser_control import *
from play_output import play
import webbrowser

urls = {
    'netflix': 'https://netflix.com',
    'google': 'https://google.com',
    'images': 'https://google.com/',
    'youtube': 'https://youtube.com',
    'videos': 'https://youtube.com',
    'video': 'https://youtube.com',
    'decathlon': 'https://decathlon.ca'
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="tiny", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large"])
    parser.add_argument("--non_english", action='store_true',
                        help="Don't use the english model.")
    parser.add_argument("--energy_threshold", default=1000,
                        help="Energy level for mic to detect.", type=int)
    parser.add_argument("--record_timeout", default=2,
                        help="How real time the recording is in seconds.", type=float)
    parser.add_argument("--phrase_timeout", default=3,
                        help="How much empty space between recordings before we "
                             "consider it a new line in the transcription.", type=float)
    args = parser.parse_args()
    
    play("Hello User, it is Santa Claus !")
    play("What would you like for Christmas ?")

    model = args.model
    if args.model != "large" and not args.non_english:
        model = model + ".en"
    audio_model = whisper.load_model(model)

    record_timeout = args.record_timeout
    phrase_timeout = args.phrase_timeout

    temp_file = NamedTemporaryFile().name
    transcription = ['']

    # The last time a recording was retreived from the queue.
    phrase_time = None
    # Current raw audio bytes.
    last_sample = bytes()
    # Thread safe Queue for passing data from the threaded recording callback.
    data_queue = Queue()

    # We use SpeechRecognizer to record our audio because it has a nice feauture where it can detect when speech ends.
    recorder = sr.Recognizer()
    recorder.energy_threshold = args.energy_threshold
    # Definitely do this, dynamic energy compensation lowers the energy threshold dramtically to a point where the SpeechRecognizer never stops recording.
    recorder.dynamic_energy_threshold = False

    source = sr.Microphone(sample_rate=16000)
    with source:
        recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio:sr.AudioData) -> None:
        """
        Threaded callback function to recieve audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        """
        # Grab the raw bytes and push it into the thread safe queue.
        data = audio.get_raw_data()
        data_queue.put(data)

    # Create a background thread that will pass us raw audio bytes.
    # We could do this manually but SpeechRecognizer provides a nice helper.
    recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

    # Cue the user that we're ready to go.
    print("Model loaded.\n")

    while True:
        try:
            now = datetime.utcnow()
            # Pull raw recorded audio from the queue.
            if not data_queue.empty():
                phrase_complete = False
                # If enough time has passed between recordings, consider the phrase complete.
                # Clear the current working audio buffer to start over with the new data.
                if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                    last_sample = bytes()
                    phrase_complete = True
                # This is the last time we received new audio data from the queue.
                phrase_time = now

                # Concatenate our current audio data with the latest audio data.
                while not data_queue.empty():
                    data = data_queue.get()
                    last_sample += data

                # Use AudioData to convert the raw data to wav data.
                audio_data = sr.AudioData(last_sample, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                wav_data = io.BytesIO(audio_data.get_wav_data())

                # Write wav data to the temporary file as bytes.
                with open(temp_file, 'w+b') as f:
                    f.write(wav_data.read())

                # Read the transcription.
                result = audio_model.transcribe(temp_file, fp16=False, language='English')
                text = result['text'].strip().lower() #.split()

                # Do stuff
                print("Output", text)
                search(text)

                #if "google" in text:
                #    print("Opening gooogle.")

                # # If we detected a pause between recordings, add a new item to our transcripion.
                # # Otherwise edit the existing one.
                # if phrase_complete:
                #     transcription.append(text)
                # else:
                #     transcription[-1] = text

                # print("Output is: ", transcription)

                # # Clear the console to reprint the updated transcription.
                # os.system('cls' if os.name=='nt' else 'clear')
                # for line in transcription:
                #     print(line)
                # # Flush stdout.
                # print('', end='', flush=True)

                # Infinite loops are bad for processors, must sleep.
                sleep(0.25)
        except KeyboardInterrupt:
            break

    print("\n\nTranscription:")
    for line in transcription:
        print(line)

def search(sentence):

    # Voice to text should go here
    sentence = sentence.lower() #'search for christmas decathlon'.lower()

    words = sentence.split(' ')
    url_key = filter_for_key(words, urls)

    # search
    if 'search' in words:
        christmas = 'christmas ' if 'christmas' in words else ''

        # user should get prompted for new sentence
        query_terms = sentence.replace('for', '').replace('christmas', '').replace('youtube', '').\
            replace('videos', '').replace('decathlon', '').replace('google', '').\
            replace('search', '').replace('images', '').replace('netflix', '').replace('video', '')
        new_sentence = christmas + query_terms

        if url_key == 'google':
            search_result = search_through_google(keyword=new_sentence)
            webbrowser.open(search_result)
        elif url_key in ['netflix', 'images']:
            webbrowser.open(search_through_google(keyword=new_sentence,
                                                  website=urls[url_key],
                                                  is_images=url_key == 'images'))
        elif url_key == 'decathlon':
            webbrowser.open(search_decathlon(keyword=new_sentence))
        elif url_key in ['youtube', 'videos', 'video']:
            webbrowser.open(search_youtube(keyword=new_sentence))

    # direct connection
    elif {'go', 'to'}.issubset(set(words)) or 'open' in words:
        webbrowser.open(urls[url_key])
    else:
        print("I don't understand")
        play("I did not understand what you have said.")


if __name__ == "__main__":
    main()