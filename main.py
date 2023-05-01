import pprint
import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import json

def get_headers():
    return Headers(browser='firefox', os='win').generate()

params = {
    'area': (1, 2),
    'text': 'python, django, flask',
    'page': 0,
    'quantity_on_page': 25
}

hh_html = requests.get('https://spb.hh.ru/search/vacancy', params=params, headers=get_headers()).text
hh_soup = BeautifulSoup(hh_html, 'lxml')
tag_vacancy = hh_soup.find('div', id='a11y-main-content')
vacancy_tags = tag_vacancy.find_all('div', class_='serp-item')

parsed_data = []

for vacancy_tag in vacancy_tags:
    h3_tag = vacancy_tag.find('h3')
    a_tag = h3_tag.find('a')
    link = a_tag['href']
    try:
        salary = vacancy_tag.find('span', class_='bloko-header-section-3').text.replace('\u202f', '')
    except:
        salary = 'Зп не указана'
    company_name = vacancy_tag.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace('\xa0', '')
    location = vacancy_tag.find('div', class_='vacancy-serp-item__info').contents[1].contents[0]
    parsed_data.append(
        {
        'ссылка': link,
        'зп': salary,
        'название компании': company_name,
        'город': location
         }
    )
pprint.pprint(parsed_data)



