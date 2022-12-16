import streamlit as st
import pandas as pd
from time import sleep
from requests import session
from bs4 import BeautifulSoup
from latest_user_agents import get_random_user_agent
ua = get_random_user_agent()
s = session()

st.set_page_config(page_title= 'Whitepages.com Scraper', page_icon=":smile:")
hide_menu = """
<style>
#MainMenu {
    visibility:hidden;}
footer {
    visibility:hidden;}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)

def scrape():
    n = 0
    item_list = []
    col1, col2 = st.columns(2)
    progress = col1.metric('Names Compared', value=0)
    for x,y in zip(all_name[:10], all_location[:10]):
        n = n + 1
        ua = get_random_user_agent()
        headers = {
        'User-Agent': ua
        }
        response = s.get(f'https://www.411.com/name/{x}/{y}', headers=headers)
        progress.metric('Names Compared', value=n)
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
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='whitepages-names.csv',
    mime='text/csv',
    )


st.title('WHITEPAGES.COM SCRAPER')
st.caption('This web app will compare names scraped from legacy.com with whitespages.com')
st.caption('Please do upload file that was scraped directly from the legacy.com, any modification to the csv file can cause an error in this web app')
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
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

button = st.button('Scrape!')

if button:
    scrape()
    st.balloons
    st.success('Done!')
