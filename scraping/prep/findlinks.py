from bs4 import BeautifulSoup
import re


def csvape():
    with open('csvape.html', 'r') as rf:
        html_content = rf.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', href=True)

    collection_links = [link['href'] for link in links if '/collections/' in link['href']]

    print(collection_links)


if __name__ == "__main__":
    csvape()
