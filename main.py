from browser_control import *
import webbrowser

urls = {
    'netflix': 'https://netflix.com',
    'google': 'https://google.com',
    'youtube': 'https://youtube.com',
    'decathlon': 'https://decathlon.ca'
}

def main():
    # Voice to text should go here
    sentence = ''.lower()
    words = sentence.split(' ')
    url = filter_for_key(words, urls)
    # search
    if 'search' in words:
        christmas = 'christmas' in words
        # user should get prompted for new sentence
        new_sentence = ''
        search_result = search_through_google(keyword = new_sentence, website = url, christmas = christmas)
        webbrowser.open(search_result)
    # direct connection
    elif {'go', 'to'}.issubset(set(words)):
        webbrowser.open(url)
    else:
        print("I don't understand")