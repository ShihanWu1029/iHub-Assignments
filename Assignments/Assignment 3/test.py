import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

def crawl_wikipedia(start_url, output_csv, max_size_mb=1):
    visited_urls = set()
    data = []
    total_size = 0

    def get_page_content(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to fetch {url}: {response.status_code}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    def parse_wikipedia_page(html):
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h1', id='firstHeading').text if soup.find('h1', id='firstHeading') else ''
        content = soup.find('div', id='bodyContent')
        paragraphs = content.find_all('p') if content else []
        text = '\n'.join([p.text for p in paragraphs])
        return title, text

    def save_to_csv(data, output_csv):
        with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Content'])
            writer.writerows(data)

    queue = [start_url]

    while queue and total_size < max_size_mb * 1024 * 1024:
        current_url = queue.pop(0)
        if current_url in visited_urls:
            continue

        visited_urls.add(current_url)
        html = get_page_content(current_url)
        if not html:
            continue

        title, text = parse_wikipedia_page(html)
        if title and text:
            data.append([title, text])
            total_size += len(text.encode('utf-8'))

        # Find links to other Wikipedia articles
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/wiki/') and ':' not in href:
                full_url = f"https://en.wikipedia.org{href}"
                if full_url not in visited_urls:
                    queue.append(full_url)

    save_to_csv(data, output_csv)
    print(f"Crawling completed. Data saved to {output_csv}")

switch = input('Scrawl?(y/n): ')
start_url = "https://en.wikipedia.org/wiki/Web_crawler"
output_csv = "./Assignments/Assignment 3/wikipedia_data.csv"

if switch == 'y' :
    crawl_wikipedia(start_url, output_csv)

df = pd.read_csv(output_csv)
all_text = ' '.join(df['Content'].dropna().tolist())
words = all_text.split()
word_counts = Counter(words)
common_words = word_counts.most_common(40)
words, counts = zip(*common_words)

plt.figure(figsize=(12, 8))
plt.bar(words, counts)
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.title('Top 40 Most Common Words in Wikipedia Dataset')
plt.xticks(rotation=45)
plt.show()