# Autocomplete API Scraper

This repository details all the steps and approaches taken while developing an optimized name extractor that scrapes names from an autocomplete API while handling rate limits, maximizing data collection, and storing results in a structured JSON file.

---

## Features
- **Efficient Prefix-Based Scraping**: Iterates through prefixes (`a-z`) to collect all possible names.
- **Multi-threaded Execution**: Runs multiple requests in parallel to speed up the process.
- **Rate Limit Handling**: Implements **exponential backoff** to retry failed requests.
- **Data Storage**: Saves extracted names into `collected_names.json`.
- **Progress Tracking**: Displays **total names collected** and **total requests made**.

---

## Tools & Technologies Used

- **Python**
  - `requests` (API calls)
  - `threading` (parallel requests)
  - `queue` (managing prefixes)
  - `json` (saving data)
  - `time` (delays & backoff)
- **JSON** (Data storage)
- **Exponential Backoff** (Handling API rate limits)

---

## How It Works

1. **Starts with a queue of `a-z`** (initial prefixes).
2. **Sends API requests** to fetch names for each prefix.
3. **Extracts unique names**, stores them, and adds new prefixes to the queue.
4. **Handles rate limits (429 errors)** using exponential backoff.
5. **Repeats until all names are collected**.
6. **Saves results in `collected_names.json`**.

---

## Challenges & Solutions

| **Challenge**            | **Solution** |
|--------------------------|-------------|
| API rate limiting (429)  | **Exponential backoff** with retries |
| Missing names            | Increased **concurrency & depth** of scraping |
| API errors & failures    | **Retry mechanism** with delays |
| Slow execution           | **Multi-threading** for parallel API calls |
