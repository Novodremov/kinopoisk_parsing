import asyncio
import os
from os.path import getsize
from time import time

import aiohttp
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from constants import DIRECTORY, NUMBER_OF_PAGES


load_dotenv()

cookie = os.getenv('COOKIE')
ua = os.getenv('UA')
user_id = os.getenv('USER_ID')


if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

HEADERS = {'cookie': cookie, 'user-agent': ua}


async def scraping_page(session, page):
    '''Скрапинг страницы с оценками.'''
    url = f'https://www.kinopoisk.ru/user/{user_id}/votes/list/vs/vote/page/{page}/perpage/{PERPAGE}/#list'
    start_time = time()
    sleep_time = 0
    while True:
        async with session.get(url, headers=HEADERS) as response:
            response_text = await response.text()
            print(f'Страница {page} загружена, время загрузки составило {time() - start_time}')
            size_of_file = await download_page(response_text, page)
            if size_of_file > 30000:
                return size_of_file
            sleep_time += 30
            print(f'Результат не достигнут. Время ожидания по странице {page} увеличено до {sleep_time}')
            await asyncio.sleep(sleep_time)


async def download_page(text, page: int):
    '''Сохранение страницы в указанную директорию.'''
    soup = BeautifulSoup(text, 'lxml')
    with open(f'{DIRECTORY}/{str(page).zfill(3)}.html', 'w', encoding='utf-8') as file:
        print(soup, file=file)
    print(f'Страница {page} сохранена')
    size_of_file = getsize(f'{DIRECTORY}/{str(page).zfill(3)}.html')
    return size_of_file


async def main():
    start_time = time()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page in range(1, NUMBER_OF_PAGES + 1):
            tasks.append(asyncio.create_task(scraping_page(session, page)))
            # await asyncio.sleep(0.5)
        result = await asyncio.gather(*tasks)
    print(f'Общее время загрузки {NUMBER_OF_PAGES} страниц составило {time() - start_time}')
    print(result)


asyncio.run(main())
