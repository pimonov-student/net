# http://stendmodel.ru/shop/bronetekhnika/1-72

# Импорты
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd


# Фильтр для цен
def price_filter(text):
    return str(text).split()[1] if ' ' in text else text


# Адрес страницы (пока без номера)
address = 'http://stendmodel.ru/shop/bronetekhnika/1-72'
# Номер текущей страницы
current_page_number = 1

total_names = []
total_prices = []

# Для использования браузера
driver = webdriver.ChromiumEdge()

while True:
    # Адрес текущей страницы
    if current_page_number != 1:
        current_page = address + f';{current_page_number}'
    else:
        current_page = address

    
    driver.get(current_page)
    html = driver.page_source
    soup = bs(html, features='html.parser')
    
    current_page_names = []
    current_page_prices = []

    for tag in soup.find_all('a', class_='product-card-title'):
        current_page_names.append(tag.text)

    for tag in soup.find_all('div', class_='price-box'):
        current_page_prices.append(price_filter(tag.text))

    total_names += current_page_names
    total_prices += current_page_prices[:]

    current_page_number += 1
    if current_page_number == 5:
        break

for i in range(len(total_prices)):
    print(total_names[i], total_prices[i])

csv_names = pd.Series(total_names)
csv_prices = pd.Series(total_prices)

csv_data = pd.DataFrame({'Names': csv_names, 'Prices': csv_prices})
csv_data.to_csv('data.csv')

driver.quit()
