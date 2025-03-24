import requests
import time
from collections import deque

BASE_URL = "http://35.200.185.69:8000/v1/autocomplete?query="
BATCH_SIZE = 5
RATE_LIMIT_DELAY = 1  # seconds
MAX_RETRIES = 3

def fetch_names(query):
    try:
        response = requests.get(BASE_URL + query)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print(f"Rate limit exceeded for query '{query}'. Retrying after delay...")
            time.sleep(RATE_LIMIT_DELAY)
            return fetch_names(query)
        else:
            print(f"Error {response.status_code} for query '{query}': {response.text}")
            return []
    except requests.RequestException as e:
        print(f"Request failed for query '{query}': {e}")
        return []

def extract_all_names():
    queue = deque([chr(i) for i in range(ord('a'), ord('z') + 1)])
    visited = set(queue)
    collected_names = set()

    while queue:
        batch = [queue.popleft() for _ in range(min(BATCH_SIZE, len(queue)))]
        for query in batch:
            retries = 0
            while retries < MAX_RETRIES:
                names = fetch_names(query)
                if names:
                    break
                retries += 1
                time.sleep(RATE_LIMIT_DELAY * retries)
            if not names:
                continue
            collected_names.update(names)
            if len(names) == 10:
                last_name = names[-1]
                if last_name not in visited:
                    queue.append(last_name)
                    visited.add(last_name)
        time.sleep(RATE_LIMIT_DELAY)

    return collected_names

if __name__ == "__main__":
    all_names = extract_all_names()
    print(f"Total names collected: {len(all_names)}")
    for name in sorted(all_names):
        print(name)
