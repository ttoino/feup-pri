from bs4 import BeautifulSoup

def raw_text(html: str):
    return BeautifulSoup(html, 'html.parser').get_text().replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
