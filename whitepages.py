from playwright.sync_api import sync_playwright
import pandas as pd
from time import sleep
from requests import session
from bs4 import BeautifulSoup
from latest_user_agents import get_random_user_agent
ua = get_random_user_agent()
s = session()

df = pd.read_csv('C:/Users/AYOMIDE/Desktop/khaliq/Joseph_app/obituary_name.csv')

first_names = df['First Name'].to_list()
last_names = df['Last Name'].to_list()
middle_names = df['Middle Name'].to_list()
cities = df['City'].to_list()
states = df['State'].to_list()

all_name = []
for x,y,z in zip(first_names, last_names, middle_names):
    name = f'{x}-{z}-{y}'
    name = name.replace('-nan', '')
    all_name.append(name)

all_location = []
for i,j in zip(cities, states):
    location = f'{i}-{j}'
    loaction = location.replace('-nan', '')
    all_location.append(location)

def scrape():
    n = 0
    item_list = []
    for x,y in zip(all_name, all_location):
        n = n + 1
        ua = get_random_user_agent()
        headers = {
        'User-Agent': ua
        }
        response = s.get(f'https://www.411.com/name/{x}/{y}', headers=headers)
        print(f'Name {n}')
        soup = BeautifulSoup(response.text, 'lxml')

        box = soup.select_one('.serp-card-wrapper')
        try:
            name = box.select_one('.name-wrap').text.split('  ')
            name = name[0]
            name = name.strip()
        except:
            name = None
        try:
            age = box.select_one('.person-age').text
        except:
            age = None
        try:
            address = box.select_one('.address-item').text.strip()
        except:
            address = None
        item = {
            'Name': name,
            'Age': age,
            'Address': address
        }
        item_list.append(item)
        sleep(1)


    df = pd.DataFrame(item_list)
    df.to_csv('legacy-whitepages.csv', index=False)
    print(df)

scrape()