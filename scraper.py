import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from urllib.parse import urldefrag
from stats import calculate_stats

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    links = set()

    if resp is None or resp.raw_response is None:
        return []

    # print(f"{resp.url} || status: {resp.status} || Error: {resp.error}")
    if resp.status != 200 or not resp.raw_response.content:
        return list(links)
    
    #Check for large files.
    max_size_bytes = 10000000 #10mb
    if len(resp.raw_response.content) > max_size_bytes:
        return list(links)

    # soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    soup = BeautifulSoup(resp.raw_response.content, 'lxml')
    readable_text = soup.get_text()

    #Check to make sure page has over 100 charcters of readable text
    if len(readable_text) < 10:
        return []

    #Checks ratio of html to human text to make sure page is not full of fluff
    # if not has_good_word_ratio(resp.raw_response.content, readable_text):
    #     return []
    
    #Only calculate stats for valid pages
    if is_valid(url):
        calculate_stats(resp, readable_text)

    for link in soup.find_all('a', href=True):
        href = link.get('href')
        defrag_url = urldefrag(href)[0]
        try:
            absolute = urljoin(resp.url, defrag_url)
        except ValueError:
            continue
        # print(url)
        
        links.add(absolute)

    return list(links)

def has_good_word_ratio(html_text, human_text):
    return len(human_text) / len(html_text) > .10

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)

        if not parsed.hostname:
            return False

        if parsed.scheme not in set(["http", "https"]):
            return False
        if not (parsed.hostname.endswith("ics.uci.edu") or parsed.hostname.endswith("cs.uci.edu") or parsed.hostname.endswith("informatics.uci.edu") 
            or parsed.hostname.endswith("stat.uci.edu") or (parsed.hostname == "today.uci.edu" and parsed.path.startswith("/department/information_computer_sciences/"))):
            return False

        #Searches for yyyy-mm-dd formats and filters out url with it
        if re.search(r"\b\d{1,4}\-\d{1,2}\-\d{1,2}\b", url.lower()) != None:
            return False

        #Searches for yyyy-dd formats and filters out url with it
        if re.search(r"\b\d{4}-\d{2}\b", url.lower()) != None:
            return False
        
        #Searches for page/(Some Nubmer) if number > 20 filters it out
        n = re.search(r"page\/(\d+)(?:\/|$)", url.lower())
        if n:
            page = int(n.group(1))
            if page > 20:
                return False
        
        #Takes to long
        if re.search(r"gitlab.ics.uci.edu|login", url) != None:
            return False

        #Billion pages of nothingness
        if re.search(r"/~eppstein/|zip-attachment|~doemer", parsed.path.lower()) != None:
            return False
        
        #Junk
        if re.search(r"(?:share=|do=|rev=|idx=|ical|action=|version=|format=txt|p=pingpong|.git)", parsed.query.lower()) != None:
            return False
        
        #IDK these killed the crawler
        if re.search(r"apk|war|img|sql|bam|ppsx", parsed.path.lower()) != None:
            return False

        #Check to remove endless reapeting url
        paths = [x for x in parsed.path.split('/') if x]
        if len(paths) > 4:
            if any(paths.count(seg) >= 2 for seg in paths):
                return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
