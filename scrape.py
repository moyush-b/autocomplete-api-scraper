import requests
import json
import time

BASE_URL = "http://35.200.185.69:8000"
VERSIONS = ["v1", "v2", "v3"]
MAX_REQUESTS = 100
COLLECTED_NAMES = {"v1": set(), "v2": set(), "v3": set()}
REQUEST_COUNTS = {"v1": 0, "v2": 0, "v3": 0}


def fetch_names(version, query):
    url = f"{BASE_URL}/{version}/autocomplete?query={query}"
    response = requests.get(url)
    REQUEST_COUNTS[version] += 1
    if response.status_code == 200:
        data = response.json()
        return set(data.get("results", []))
    return set()


def expand_prefixes(version, prefix, depth=2):
    queue = [prefix]
    visited = set()

    while queue and REQUEST_COUNTS[version] < MAX_REQUESTS:
        current_prefix = queue.pop(0)
        if current_prefix in visited:
            continue
        visited.add(current_prefix)

        names = fetch_names(version, current_prefix)
        new_names = names - COLLECTED_NAMES[version]
        COLLECTED_NAMES[version].update(new_names)

        if len(names) == 10:  # Assuming API returns a max of 10 results
            for char in "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+":
                new_prefix = current_prefix + char
                if new_prefix not in visited:
                    queue.append(new_prefix)


def main():
    for version in VERSIONS:
        expand_prefixes(version, "", depth=3)

    with open("collected_names.json", "w") as f:
        json.dump({k: list(v) for k, v in COLLECTED_NAMES.items()}, f, indent=4)

    print("Total names collected:")
    for version in VERSIONS:
        print(f"{version}: {len(COLLECTED_NAMES[version])}")

    print("\nTotal requests made:")
    for version in VERSIONS:
        print(f"{version}: {REQUEST_COUNTS[version]}")


if __name__ == "__main__":
    main()
