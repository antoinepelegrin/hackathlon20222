from googlesearch import search


def filter_for_key(words: list, dictionary: dict):
    for word in words:
        if word.lower() in dictionary:
            return dictionary[word.lower()]
    return dictionary['google']


def search_through_google(keyword: str, website: str, christmas: bool = False):
    christmas = 'christmas' if christmas else ''
    search_results = search(f'site:{website} {christmas} {keyword}')
    return search_results[0]
