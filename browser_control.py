def filter_for_key(words: list, dictionary: dict):
    for word in words:
        if word.lower() in dictionary:
            return dictionary[word.lower()]
    return dictionary['google']


def search_through_google(keyword: str, website: str = None, is_christmas: bool = False, is_images: bool = False):
    christmas = 'christmas ' if is_christmas else ''
    site = f'site:{website} : ' if website is not None else ''
    search_option = 'search?tbm=isch&as_q=' if is_images else 'search?q='
    search_url = f'https://www.google.com/{search_option}{site}{christmas}{keyword}'
    return search_url
