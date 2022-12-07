from browser_control import *
from play_output import play_sound
import webbrowser

urls = {
    'netflix': 'https://netflix.com',
    'google': 'https://google.com',
    'image': 'https://www.google.com/imghp',
    'youtube': 'https://youtube.com',
    'decathlon': 'https://decathlon.ca'
}

def main():

    play_sound("hello_user")
    play_sound("help_you")

    # Voice to text should go here
    sentence = ''.lower()

    words = sentence.split(' ')
    url = filter_for_key(words, urls)

    # search
    if 'search' in words:
        christmas = 'christmas' in words
        # user should get prompted for new sentence
        new_sentence = ''

        search_result = search_through_google(keyword=new_sentence, website=url, christmas=christmas)
        webbrowser.open(search_result)

    # direct connection
    elif {'go', 'to'}.issubset(set(words)):
        webbrowser.open(url)

    else:
        play_sound("I_do_not_understand")