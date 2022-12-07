from browser_control import *
#from output import play_sound
import webbrowser

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
    
    #play_sound("hello_user")
    #play_sound("help_you")

    # Voice to text should go here
    sentence = 'search for christmas youtube videos'.lower()

    words = sentence.split(' ')
    url_key = filter_for_key(words, urls)

    # search
    if 'search' in words:
        christmas = 'christmas ' if 'christmas' in words else ''

        # user should get prompted for new sentence
        new_sentence = christmas + 'cats'

        if url_key == 'google':
            search_result = search_through_google(keyword=new_sentence)
            webbrowser.open(search_result)
        elif url_key in ['netflix', 'images']:
            webbrowser.open(search_through_google(keyword=new_sentence,
                                                  website=urls[url_key],
                                                  is_images=url_key=='images'))
        elif url_key == 'decathlon':
            webbrowser.open(get_decathlon_link(keyword=new_sentence))
        elif url_key == 'youtube':
            webbrowser.open(get_youtube_link(keyword=new_sentence))

    # direct connection
    elif {'go', 'to'}.issubset(set(words)) or 'open' in words:
        webbrowser.open(ulrs[url_key])
    else:
        print("I don't understand")
        #play_sound("I_do_not_understand")

main()
