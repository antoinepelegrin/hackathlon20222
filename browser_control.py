

def filter_for_key(words: list, dictionary: dict):
    for word in words:
        if word.lower() in dictionary:
            return word.lower()
    return 'google'


def search_through_google(keyword: str, website: str = None, is_images: bool = False):
    site = f'site:{website} ' if website is not None else ''
    search_option = 'search?tbm=isch&as_q=' if is_images else 'search?q='
    search_url = f'https://www.google.com/{search_option}{site}{keyword}'
    return search_url


def search_decathlon(keyword: str):
    word_list = keyword.split(' ')
    query = ''
    for word in word_list:
        query+= word + '%20'
    url = f'https://www.decathlon.ca/en/search?query={query}'
    return url


def search_youtube(keyword: str):
    word_list = keyword.split(' ')
    query = ''
    for word in word_list:
        query+= word + '+'
    url = f'https://www.youtube.com/results?search_query={query}'

    return url