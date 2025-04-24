from bs4 import BeautifulSoup
from urllib.parse import urlparse

UNIQUE_PAGES = 0
LONGEST_PAGE = 0
LONGEST_PAGE_COUNT = 0
PAGES = {}
COMMON_WORDS = {}
SUBDOMAINS = {}
ENGLISH_STOP_WORDS = {}

def calculate_stats(resp):

    soup = BeautifulSoup(resp.raw_response.content, 'html.parser')

    parsed_url = urlparse(resp.raw_response.url)
    parsed_url._replace(fragment="").geturl()
    unique_pages(parsed_url)
    
    '''
    text = soup.get_text()
    tokens = tokenizer(text)
    calculate_num_words(tokens)

    '''
    pass

def unique_pages(url) -> None:
    PAGES.add(url)
    UNIQUE_PAGES = len(PAGES)

def calculate_num_words(url, tokens) -> None:
    word_count = len(tokens)

    if word_count > LONGEST_PAGE_COUNT:
        LONGEST_PAGE_COUNT = word_count
        LONGEST_PAGE = url

def common_words():
    '''

    '''
    pass

def computeWordFrequencies(TokenList) -> None:
    for word in TokenList:
        if not word in ENGLISH_STOP_WORDS:
            COMMON_WORDS[word] = COMMON_WORDS.get(word, 0) + 1


def write_stats():
    pass