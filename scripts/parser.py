import requests
from bs4 import BeautifulSoup
import json
import time


# TODO: Testing TODO functionality


def write_to_file(name, text_to_write, path, formatting='.txt'):
    """Creating text file with current name in 'path' directory and write text into it."""
    with open(path + name + formatting, 'w', encoding='utf-8') as file:
        file.write(text_to_write)


def get_html(url):
    """Returns HTML-code of incoming url."""
    try:
        return requests.get(url).text
    except:
        return None


# Setting default values from config file to variables

with open("config.json", 'r', encoding='utf-8') as f:
    data = json.load(f)
    contentPath = data["defaultContentPath"]
    htmlPath = data["defaultHtmlPath"]
    defaultUrl = data["defaultUrl"]

html = getHtml(defaultUrl)
write_to_file(BeautifulSoup(html, 'lxml').title.text.split('/')[0], html, htmlPath, '.html')

# Opening local main page HTML
# with open("K:\Projects\Scrapper\scripts\data\Лучшие публикации за сутки .html", 'r', encoding = 'utf-8') as f:
# html = f.read()


soup = BeautifulSoup(html, "lxml")
links = {}

# Collecting all links from the main page

for ref in soup.find('div', class_='dropdown-container dropdown-container_flows').find_all(
        class_='n-dropdown-menu__item-link n-dropdown-menu__item-link_flow'):
    text = ref.text
    link = ref.get('href')
    links.update({text: link})

print('Starting...')
catalogName = 'Catalog'
countGet = int(input('Ввести количество страниц, с которых необходимо получить статьи (1-5):'))
cGet = 0

# Downloading HTML's of all references and saving in files

for newUrl in links.values():
    print(newUrl)
    cGet += 1
    currentPage = getHtml(newUrl)
    currentSoup = BeautifulSoup(getHtml(newUrl), 'lxml')
    write_to_file(BeautifulSoup(currentPage, 'lxml').title.text.split('/')[0].split(' ')[-2], currentPage, htmlPath,
                  '.html')
    try:
        # Getting titles and content of all posts and saving in own files
        for topic in currentSoup.find('div', class_='posts_list').find_all('li'):
            try:
                # print(type(topic), topic)
                # print(topic.find('h2', class_='post__title').find('a').get('href'))

                topicUrl = topic.find('h2', class_='post__title').find('a').get('href')
                topicHtml = getHtml(topicUrl)
                topicSoup = BeautifulSoup(topicHtml, 'lxml')
                topicName = topicSoup.title.text.split('/')[0]
                if topicSoup.find('div', class_='company_post') is not None:
                    continue
                topicText = topicSoup.find('div', class_='post__text post__text-html js-mediator-article').get_text()
                # print(topicName)
                # print(topicText)
                write_to_file(topicName, topicText, contentPath)
                currentTime = time.asctime()
                with open(contentPath + catalogName + '.txt', 'a', encoding='utf-8') as s:
                    s.write(topicName + currentTime + '\n')
            except:
                continue
            print('End of topic...')
    except:
        continue
    if countGet == cGet:
        break

# Saving site sections in config file

with open('References.json', 'w', encoding='utf-8') as f:
    json.dump(links, f, sort_keys=True, indent=4, ensure_ascii=False)
    # print(ref.text)
    # print(ref.get('href'))

print('Jobs done')
