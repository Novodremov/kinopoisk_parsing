import csv

import pandas as pd
from bs4 import BeautifulSoup

from constants import DIRECTORY, NUMBER_OF_PAGES


def parsing_movie(movie):
    """Извлечение информации по фильму из html-кода с помощью тегов."""
    series = '-'
    name_rus_year = movie.find(class_='nameRus').text
    open_par = name_rus_year.rfind('(')
    name_rus, year = (name_rus_year[:open_par - 1],
                      name_rus_year[open_par + 1:-1])
    if not year.replace('–', '').replace('-', '').replace(' ', '').isdigit():
        series, year = (x.strip() for x in year.split(','))
    name_eng = movie.find(class_='nameEng').text
    link = 'https://www.kinopoisk.ru' + movie.find('a')['href']
    rating = movie.find('b')
    rating = rating.text if rating else '-'
    text_grey = [x.text for x in movie.find_all(class_='text-grey')]
    if text_grey:
        votes, duration = (
            ('-', text_grey[0]) if len(text_grey) == 1 else text_grey)
    else:
        votes, duration = '-', '-'
    votes = votes.strip('()')
    date_of_vote = movie.find('div', class_='date').text
    my_vote = movie.find('div', class_='vote').text
    return (name_rus, name_eng, year, my_vote, date_of_vote, rating, votes,
            series, link)


def writing_page_to_csv(page, number):
    print('Пишем страницу', page)
    with open(f'{DIRECTORY}/{str(page).zfill(3)}.html', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')
        # вытаскиваем куски html, касающиеся фильмов:
        movies = soup.find_all('div', class_='item')
        rows = []
        for movie in movies:
            rows.append((number,) + parsing_movie(movie))
            number += 1
        return rows, number


columns = ('№', 'Русскоязычное название', 'Оригинальное название', 'Год',
           'Моя оценка', 'Дата оценки', 'Рейтинг', 'Число оценок', 'Сериал',
           'Ссылка на страницу фильма')
with open('movies.csv', 'w', encoding='utf-8-sig') as registry:
    writer = csv.writer(registry, delimiter=';')
    writer.writerow(columns)
    number = 1
    for page in range(1, NUMBER_OF_PAGES + 1):
        rows, number = writing_page_to_csv(page, number)
        writer.writerows(rows)

df = pd.read_csv('movies.csv', delimiter=';')
df.to_excel('movies.xlsx', index=False)
