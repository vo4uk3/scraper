import os
import requests as requests
from bs4 import BeautifulSoup


def get_info(pages, art_type ,url):
    print(os.getcwd())

    # getting links to pages
    links = []
    page_url = '?searchType=journalSearch&sort=PubDate&page={page}'
    page = 1
    while page <= pages:
        links.append(url + page_url.format(page=page))
        print('Creating directory' + str(page))
        os.mkdir(f'Page_{page}')
        os.chdir(os.getcwd() + f'/Page_{page}')


        # getting articles types from the page
        for link in links:
            response = requests.get(link,headers={'Accept-Language': 'en-US,en;q=0.5'})
            soup = BeautifulSoup(response.content, 'html.parser')
            news = []
            for i in soup.findAll('article'):
                if i.find('span', {'class':'c-meta__type'}).text == art_type:
                    news.append(i)

            # getting article text and writing files
            files = list()
            for k in news:
                name = k.find('a', {"data-track-action":"view article"}).text.replace(' ', '_')
                req = 'https://www.nature.com'+ k.find('a').get('href')
                responce = requests.get(req)
                article = BeautifulSoup(responce.content, 'html.parser')
                test = article.find('div', {'class': 'c-article-body'})
                if test is None:
                    test = article.find('div', {'class' : 'article-item__body'})
                if test is None:
                    test = article.find('article').text
                with open(f'{name}.txt', 'w') as result:
                    result.writelines(test)
                    files.append(result)
        page += 1
        os.chdir(os.path.split(os.getcwd())[0])


if __name__ == '__main__':
     get_info(int(input()),input() , 'https://www.nature.com/nature/articles')
