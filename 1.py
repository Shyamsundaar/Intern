import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import time

def scrape_website(url):
    # Send a GET request to the website and get the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all the articles on the page
    articles = soup.find_all('article')
    
    # Create an empty list to store the data
    data = []
    
    # Loop through each article and extract the required data
    for article in articles:
        headline = article.find('h2').text.strip()
        link = article.find('a')['href']
        author = article.find('span', class_='c-byline__author-name').text.strip()
        date = article.find('time')['datetime']
        
        # Create a dictionary to store the data for each article
        article_data = {
            'headline': headline,
            'link': link,
            'author': author,
            'date': date
        }
        
        # Append the dictionary to the list of data
        data.append(article_data)
        
    return data

url = 'https://www.theverge.com'
data = scrape_website(url)

filename = time.strftime("%d%m%Y") + '_verge.csv'
with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['id', 'URL', 'headline', 'author', 'date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i, row in enumerate(data):
        writer.writerow({'id': i+1, 'URL': row['link'], 'headline': row['headline'], 'author': row['author'], 'date': row['date']})

conn = sqlite3.connect('verge_articles.db')
c = conn.cursor()

c.execute('''CREATE TABLE articles
             (id INTEGER PRIMARY KEY,
              URL TEXT,
              headline TEXT,
              author TEXT,
              date TEXT)''')

conn.commit()

article_data = [(i+1, row['link'], row['headline'], row['author'], row['date']) for i, row in enumerate(data)]

c.executemany('INSERT INTO articles VALUES (?, ?, ?, ?, ?)', article_data)

conn.commit

