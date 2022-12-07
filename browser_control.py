import webbrowser
from googlesearch import search

direct_urls = {
    'netflix': 'https://netflix.com',
    'google': 'https://google.com',
    'youtube': 'https://youtube.com',
}

search_engines = {

}

def filter_for_key(sentence: str, dictionary: dict):
    words = sentence.split(' ')
    for word in words:
        if word.lower() in dictionary:
            return word
    return 'google'

def search_through_google(keyword: str, website: str):
    return

def open_page(key: str):
    try:
        webbrowser.open(urls[key])
    except KeyError:
        print(f"Can't open {key}")

