from bs4 import BeautifulSoup
from urllib.parse import urlparse

UNIQUE_PAGES = 0
LONGEST_PAGE = 0
LONGEST_PAGE_COUNT = 0
PAGES = {}
COMMON_WORDS = {}
SUBDOMAINS = {}
#Note words with ' will not be filtered out because of tokenizer treating it as seperator
ENGLISH_STOP_WORDS = stopwords = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than",
    "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
    "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've",
    "this", "those", "through", "to", "too", "under", "until", "up", "very", "was",
    "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what",
    "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's",
    "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd",
    "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
}

def calculate_stats(resp):

    soup = BeautifulSoup(resp.raw_response.content, 'html.parser')

    parsed_url = urlparse(resp.raw_response.url)
    subdomain = parsed_url.hostname.split('.')[0]
    parsed_url._replace(fragment="").geturl()
    unique_pages(parsed_url)
    
    '''
    text = soup.get_text()
    tokens = tokenizer(text)
    calculate_num_words(tokens)

    '''


def unique_pages(url) -> None:
    PAGES.add(url)
    UNIQUE_PAGES = len(PAGES)


def calculate_num_words(url, tokens) -> None:
    word_count = len(tokens)

    if word_count > LONGEST_PAGE_COUNT:
        LONGEST_PAGE_COUNT = word_count
        LONGEST_PAGE = url


def calcuate_subdomains(subdomain):
    SUBDOMAINS[subdomain] = SUBDOMAINS.get(subdomain, 0) + 1


def computeWordFrequencies(TokenList) -> None:
    for word in TokenList:
        if not word in ENGLISH_STOP_WORDS:
            COMMON_WORDS[word] = COMMON_WORDS.get(word, 0) + 1


def tokenize(text) -> list:
    tokens = []
    word = ""
    word_chars = []
        for char in line:
            if (char.isascii() and char.isalnum()):
                word_chars.append(char)
            else:
                if word_chars:
                    tokens.append("".join(word_chars).lower())
                    word_chars = []
        # Append last word if exists
        if word_chars:
            tokens.append("".join(word_chars).lower())
    return tokens


def write_stats():
    pass