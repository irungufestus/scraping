import urllib.request
from urllib import robotparser
from urllib.error import URLError, HTTPError, ContentTooShortError 
import re

def download(url, user_agent='wswp', num_retries=2, charset='utf-8'):
    print('Downloading:', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)
    try:
        resp = urllib.request.urlopen(request)
        cs = resp.headers.get_content_charset()
        if not cs:
            cs = charset
            html = resp.read().decode(cs)
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
    if num_retries > 0:
        if hasattr(e, 'code') and 500 <= e.code < 600:
        # recursively retry 5xx HTTP errors
            return download(url, num_retries - 1)
    return html
def crawl_sitemap(url):
    # download the sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    # download each link
    for link in links:
        html = download(link)
        # scrape html here
        # ...
def get_robots_parser(robots_url):
    " Return the robots parser object using the robots_url "
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp
def link_crawler(start_url, link_regex, robots_url=None,
    user_agent='wswp'):
    ...
    if not robots_url:
        robots_url = '{}/robots.txt'.format(start_url)
        rp = get_robots_parser(robots_url)
        #Finally, we add the parser check in the crawl loop:
    ...
    while crawl_queue:
        url = crawl_queue.pop()
        # check url passes robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            html = download(url, user_agent=user_agent)
            ...
        else:
            print('Blocked by robots.txt:', url)


