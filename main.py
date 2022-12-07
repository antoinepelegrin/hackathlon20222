from browser_control import *
from play_output import play
import webbrowser
import time

urls = {
    'netflix': 'https://netflix.com',
    'google': 'https://google.com',
    'images': 'https://www.google.com/imghp',
    'youtube': 'https://youtube.com',
    'decathlon': 'https://decathlon.ca'
}

# example inputs:
# go to decathlon, go to google
# search Youtube -> cat
# search for Christmas images -> cat -> christmas cat
def main():

    play("Hello User, it is Santa Claus !")
    play("What would you like for Christmas ?")

    # Voice to text should go here
    sentence = 'search for christmas decathlon'.lower()

    words = sentence.split(' ')
    url = filter_for_key(words, urls)

    # search
    if 'search' in words:
        is_christmas = 'christmas' in words
        is_images = 'images' in words
        # user should get prompted for new sentence
        new_sentence = 'cats'

        url = url if url not in [urls['google'], urls['images']] else None

        search_result = search_through_google(keyword=new_sentence, website=url, is_christmas=is_christmas, is_images=is_images)
        webbrowser.open(search_result)

    # direct connection
    elif {'go', 'to'}.issubset(set(words)) or 'open' in words:
        webbrowser.open(url)
    else:
        print("I don't understand")
        play("I_do_not_understand")

main()        
