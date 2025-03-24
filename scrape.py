import requests
import time
import json

def fetch_names(api_version, query, seen_names, total_requests):
    url = f"http://35.200.185.69:8000/{api_version}/autocomplete?query={query}"
    response = requests.get(url)
    total_requests[api_version] += 1
    
    if response.status_code != 200:
        print(f"Error: {response.status_code} for {query} in {api_version}")
        return []
    
    try:
        data = response.json()
        return [name for name in data.get("results", []) if name not in seen_names]
    except json.JSONDecodeError:
        print("Failed to parse JSON response")
        return []

def extract_all_names():
    versions = ["v1", "v2", "v3"]
    seen_names = {v: set() for v in versions}
    total_requests = {v: 0 for v in versions}
    queue = {v: [""] for v in versions}  # Start with an empty query
    
    while any(queue.values()):
        for v in versions:
            if not queue[v]:
                continue
            
            query = queue[v].pop(0)
            new_names = fetch_names(v, query, seen_names[v], total_requests)
            
            for name in new_names:
                if name not in seen_names[v]:
                    seen_names[v].add(name)
                    queue[v].append(name)  # Use names as new queries for deeper discovery
            
            time.sleep(0.1)  # Prevent hitting rate limits
    
    return seen_names, total_requests

def main():
    all_names, requests_made = extract_all_names()
    
    for v in all_names:
        print(f"Total names collected in {v}: {len(all_names[v])}")
    
    for v in requests_made:
        print(f"Total requests made to {v}: {requests_made[v]}")
    
    with open("extracted_names.json", "w") as f:
        json.dump(all_names, f, indent=4)

if __name__ == "__main__":
    main()
