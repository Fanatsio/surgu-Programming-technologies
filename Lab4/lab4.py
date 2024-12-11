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

    def save_urls_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for url in self.urls:
                f.write(url + '\n')

class URLStateMachine(URLFinder):
    def __init__(self, url, depth):
        super().__init__(url, depth)
        self.state = 'INIT'
        self.transitions = {
            'INIT': self.init_state,
            'RECURSIVE_FETCH': self.recursive_fetch_state,
            'DONE': self.done_state
        }

    def run(self):
        while self.state != 'DONE':
            self.transitions[self.state]()

    def init_state(self):
        self.state = 'RECURSIVE_FETCH'

    def recursive_fetch_state(self, current_url=None, current_depth=None):
        if current_url is None and current_depth is None:
            current_url, current_depth = self.url, self.depth

        if current_url in self.visited or current_depth == 0:
            return

        self.visited.add(current_url)
        html_content = self.fetch_url(current_url)
        if html_content:
            urls_found = self.parse_urls(html_content)
            self.urls.update(urls_found)
            for url_found in urls_found:
                print(url_found)
                self.recursive_fetch_state(url_found, current_depth - 1)

        if current_url == self.url:
            self.state = 'DONE'

    def done_state(self):
        print("FSM done.")

def test_algorithm(url, depth):
    fsm_finder = URLStateMachine(url, depth)

    start_time = time.time()
    fsm_finder.run()
    fsm_time = time.time() - start_time

    print("-" * 20)
    print(f"URLs found: {len(fsm_finder.urls)}")
    print(f"Time taken by Finite State Machine algorithm: {fsm_time:.2f} seconds")

    filename_fsm = "found_urls_fsm.txt"
    fsm_finder.save_urls_to_file(filename_fsm)
    print(f"Found URLs (FSM) saved to {filename_fsm}")

if __name__ == "__main__":
    test_algorithm("https://en.wikipedia.org/wiki/List_of_Hindi_songs_recorded_by_Asha_Bhosle", 2)
