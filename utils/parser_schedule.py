import requests
import re
from bs4 import BeautifulSoup


class Lesson:
    def __init__(self, lesson_number=None, lesson_time=None, lesson_date=None, lesson_way=None, lesson_content=None):
        self.date = lesson_date
        self.number = lesson_number
        self.time = lesson_time
        self.content = lesson_content
        self.way = lesson_way


def _parse_page(page):
    table = page.find('table', attrs={'cellpadding': 1})

    lessons = []
    date = None
    for i in table.find_all('tr'):
        match = re.search(r'(\d+\.\d+\.\d{4})', i.text)
        if match:
            date = match.group()
        if i.has_attr('align'):
            if not i.text.find('№'):
                continue
            less = Lesson()
            less.date = date
            for index, lesson in enumerate(i.find_all('td')):
                if index == 0:
                    less.number = lesson.text.strip()
                if index == 1:
                    less.time = lesson.text.strip().replace('\t', '')
                if index == 2:
                    less.way = lesson.text.strip()
                if index == 3:
                    less.content = lesson.text.strip()
                if index == 4:
                    break
            lessons.append(less)
    return lessons


def get_lessons(url):
    lessons = []

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    lessons.extend(_parse_page(soup))

    link_next_week = 'https://lk.ks.psuti.ru/' + soup.find('a', string='следующая неделя')['href']

    page = requests.get(link_next_week)
    soup = BeautifulSoup(page.text, 'lxml')
    lessons.extend(_parse_page(soup))
    return lessons


def get_lessons_week(url):
    lessons = []

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    lessons.extend(_parse_page(soup))

    return lessons


def get_link_schedule_group(group):
    page = requests.get('https://lk.ks.psuti.ru/')
    soup = BeautifulSoup(page.text, 'lxml')
    tags = soup.find_all('a')
    for tag in tags:
        if tag.text.lower() == group.lower():
            return 'https://lk.ks.psuti.ru/' + tag['href']
    return None
