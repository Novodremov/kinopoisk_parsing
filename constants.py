from math import ceil

DIRECTORY = 'kinopoisk_pages'  # Название директории для загрузки страниц

NUMBER_OF_SCORES = 8400  # Число оценок на Кинопоиске
PERPAGE = 200
NUMBER_OF_PAGES = ceil(NUMBER_OF_SCORES / PERPAGE)
