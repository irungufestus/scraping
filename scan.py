from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup


def get_html(page):
    url = f"https://books.toscrape.com/catalogue/category/books/fiction_{page}/index.html"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup
  

def main():
    html=get_html(1)
    print (html)

if __name__=='__main__':
    main()
