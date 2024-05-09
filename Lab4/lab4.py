import requests
from bs4 import BeautifulSoup
import time

class URLFinder:
    def __init__(self, url, depth):
        self.url = url
        self.depth = depth
        self.urls = set()
        self.visited = set()

    def fetch_url(self, url):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
        return None

    def parse_urls(self, html_content):
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        urls_found = [link.get('href') for link in soup.find_all('a', href=True)]
        return [url for url in urls_found if url.startswith('http')]

    def dfs(self, current_url, current_depth):
        if current_url in self.visited or current_depth == 0:
            return
        self.visited.add(current_url)

        html_content = self.fetch_url(current_url)
        if html_content:
            urls_found = self.parse_urls(html_content)
            self.urls.update(urls_found)
            for url_found in urls_found:
                print(url_found)
                self.dfs(url_found, current_depth - 1)

    def find_urls_fsm(self):
        self.dfs(self.url, self.depth)

    def find_urls_naive(self):
        html_content = self.fetch_url(self.url)
        if html_content:
            urls_found = self.parse_urls(html_content)
            self.urls.update(urls_found)
            for url_found in urls_found:
                print(url_found)

    def save_urls_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for url in self.urls:
                f.write(url + '\n')

def test_algorithm(url, depth):
    finder = URLFinder(url, depth)

    start_time = time.time()
    finder.find_urls_fsm()
    fsm_time = time.time() - start_time

    start_time = time.time()
    finder.find_urls_naive()
    naive_time = time.time() - start_time

    print("-" * 20)
    print(f"URLs found using Finite State Machine algorithm: {len(finder.urls)}")
    print(f"URLs found using Naive algorithm: {len(finder.urls)}")

    print(f"Time taken by Finite State Machine algorithm: {fsm_time:.2f} seconds")
    print(f"Time taken by Naive algorithm: {naive_time:.2f} seconds")

    filename = "found_urls.txt"
    finder.save_urls_to_file(filename)
    print(f"Found URLs saved to {filename}")

if __name__ == "__main__":
    test_algorithm("https://en.wikipedia.org/wiki/List_of_Hindi_songs_recorded_by_Asha_Bhosle", 2)
