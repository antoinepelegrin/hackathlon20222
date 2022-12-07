from browser_control import *
#from play_output import play
import webbrowser
import time

urls = {
    'netflix': 'https://netflix.com',
    'google': 'https://google.com',
    'images': 'https://www.google.com/imghp',
    'youtube': 'https://youtube.com',
    'videos': 'https://youtube.com',
    'decathlon': 'https://decathlon.ca'
}

# example inputs:
# go to decathlon, go to google
# search Youtube -> cat
# search for Christmas images -> cat -> christmas cat
def main():

    #play("Hello User, it is Santa Claus !")
    #play("What would you like for Christmas ?")

    # Voice to text should go here
    sentence = 'search for christmas horses videos'.lower()

    words = sentence.split(' ')
    url_key = filter_for_key(words, urls)

    # search
    if 'search' in words:
        christmas = 'christmas ' if 'christmas' in words else ''

        # user should get prompted for new sentence
        query_terms = sentence.replace('for', '').replace('christmas', '').replace('youtube', '').\
            replace('videos', '').replace('decathlon', '').replace('google', '').\
            replace('search', '').replace('images', '').replace('netflix', '')
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
        #play("I_do_not_understand")

main()
