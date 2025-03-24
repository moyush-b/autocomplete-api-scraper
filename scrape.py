import requests
import time
import threading
import json
from queue import Queue

API_URL = "http://35.200.185.69:8000/v1/autocomplete?query="  # Change v1, v2, v3 as needed

collected_names = set()
searched_prefixes = set()
queue = Queue()

for letter in "abcdefghijklmnopqrstuvwxyz":
    queue.put(letter)

request_count = 0
names_pulled_count = 0
INITIAL_CONCURRENCY = 3
concurrency_limit = INITIAL_CONCURRENCY
lock = threading.Lock()

def delay(ms):
    time.sleep(ms / 1000)

def fetch_names(prefix, attempt=1):
    global request_count, names_pulled_count

    if prefix in searched_prefixes:
        return
    searched_prefixes.add(prefix)

    try:
        with lock:
            request_count += 1
        response = requests.get(API_URL + prefix, timeout=5)

        if response.status_code == 429:
            wait_time = min(500 * attempt, 6000)
            print(f"Rate limited on: {prefix}. Retrying in {wait_time / 1000}s...")
            delay(wait_time)
            return fetch_names(prefix, attempt + 1)

        response.raise_for_status()
        data = response.json()
        new_names = []

        if "results" in data:
            for name in data["results"]:
                if name not in collected_names and len(name) > len(prefix):
                    with lock:
                        collected_names.add(name)
                        names_pulled_count += 1
                    new_names.append(name)

        if len(new_names) >= 5:
            for name in new_names:
                queue.put(name[:len(prefix) + 1])

    except requests.RequestException as error:
        print(f"Error fetching {prefix}: {error}")

def save_names_to_file():
    with open("collected_names.json", "w", encoding="utf-8") as f:
        json.dump(sorted(collected_names), f, indent=4)
    print("\n✅ Names saved to collected_names.json")

def discover_names():
    while not queue.empty():
        batch = [queue.get() for _ in range(min(concurrency_limit, queue.qsize()))]
        print(f"Fetching names for: {batch}")

        threads = []
        for prefix in batch:
            thread = threading.Thread(target=fetch_names, args=(prefix,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        delay(300)

    save_names_to_file()
    print(f"\n🚀 Extraction Complete!")
    print(f"📌 Total names collected: {len(collected_names)}")
    print(f"🔄 Total requests made: {request_count}")

if __name__ == "__main__":
    discover_names()
