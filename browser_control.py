import webbrowser

urls = {
    'netflix': 'https://netflix.com',
    'google': 'https://google.com',
    'youtube': 'https://youtube.com',
}


def filter_for_key(sentence: str):
    words = sentence.split(' ')
    for word in words:
        if word in urls:
            return word


def open_page(key: str):
    try:
        webbrowser.open(urls[key])
    except KeyError:
        print(f"Can't open {key}")