import requests
import json
import time
from collections import deque

def fetch_names(version, prefix, seen_names, base_url, request_count):
    url = f"{base_url}/{version}/autocomplete?query={prefix}"
    response = requests.get(url)
    request_count[version] += 1
    
    if response.status_code != 200:
        return []
    
    data = response.json()
    new_names = data.get("results", [])
    
    unique_new_names = [name for name in new_names if name not in seen_names]
    seen_names.update(unique_new_names)
    return unique_new_names

def extract_all_names(version, base_url):
    seen_names = set()
    queue = deque([chr(i) for i in range(97, 123)])  # Start with 'a' to 'z'
    request_count = {"v1": 0, "v2": 0, "v3": 0}
    
    while queue:
        prefix = queue.popleft()
        new_names = fetch_names(version, prefix, seen_names, base_url, request_count)
        
        for name in new_names:
            if len(name) > len(prefix):  # Expand further
                queue.append(name)
    
    return seen_names, request_count[version]

def main():
    base_url = "http://35.200.185.69:8000"
    all_results = {}
    total_requests = {}
    
    for version in ["v1", "v2", "v3"]:
        names, request_count = extract_all_names(version, base_url)
        all_results[version] = list(names)
        total_requests[version] = request_count
    
    print("Total names collected:")
    for version in all_results:
        print(f"{version}: {len(all_results[version])}")
    
    print("Total requests made:")
    for version in total_requests:
        print(f"{version}: {total_requests[version]}")
    
    with open("collected_names.json", "w") as f:
        json.dump(all_results, f, indent=4)
    
if __name__ == "__main__":
    main()
