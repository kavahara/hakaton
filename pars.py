from bs4 import BeautifulSoup as BS
import  requests
import csv

def get_html(url):
    response = requests.get(url)
    return response.text

def get_data(html):
    soup = BS(html, 'lxml')
    catalog = soup.find('div', class_='search-results-table')
    cars = catalog.find_all('div', class_='list-item list-label')
    for car in cars:
        try:
            tittle = car.find('h2', class_='name').text.strip()
        except:
            tittle = ''
        try:
            price = car.find('p', class_='price').get('strong').text.strip()
        except:
            price = ''
        try:
            img = car.find('div', class_='thumb-item-carousel').find('img').get('data-src')
        except:
            img = ''
        try:
            year = car.find('p', class_='year-miles').text.strip()
            kuzov = car.find('p', class_='body-type').text.strip()
            km = car.find('p', class_='volume').text.strip()
        except:
            year = ''
            kuzov = ''
            km = ''

        data = {
            'tittle': tittle,
            'price': price,
            'img': img,
            'year': year,
            'kuzov': kuzov,
            'km': km
        }

        write_csv(data)

def write_csv(data):
    with open('cars.csv', 'a', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter='/')
        writer.writerow((data['tittle'], data['price'], data['img'], data['year'], data['kuzov'], data['km']))

def main():
    for page in range(1, 856):
        url = f'https://www.mashina.kg/search/all/?page={page}'
        html = get_html(url)
        data = get_data(html)
main()