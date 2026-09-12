# Automated Bitcoin Price Scraper

A Python scraper that pulls the live Bitcoin price from [CoinMarketCap](https://coinmarketcap.com/currencies/bitcoin/) on a timed loop and appends every reading to a CSV, building a timestamped price history that can be opened directly in Excel or loaded back into Pandas for analysis.

Instead of checking a price page by hand, the script collects the data for you — one row every 10 seconds, for as long as it runs.

**[View the code](Crypto%20Web%20Scraper.py)** · **[View the collected data](Auto%20Crypto%20Web%20Scraper.csv)**

---

## What it does

1. Requests the CoinMarketCap Bitcoin page and parses the HTML with BeautifulSoup
2. Extracts the coin name and current price, stripping out the `$` and the trailing "price" text
3. Stamps the reading with the exact capture time from `datetime.now()`
4. Writes the row to a CSV — creating the file with headers on the first run, appending without headers on every run after
5. Sleeps 10 seconds and repeats

## Sample output

The included dataset was captured over a ~6 minute run on June 28, 2024 (34 readings):

| Crypto Name | Price     | Time Stamp                 |
|-------------|-----------|----------------------------|
| Bitcoin     | 60,738.04 | 2024-06-28 14:17:52.548615 |
| Bitcoin     | 60,739.05 | 2024-06-28 14:19:25.179027 |
| Bitcoin     | 60,715.05 | 2024-06-28 14:21:39.417733 |
| Bitcoin     | 60,638.43 | 2024-06-28 14:23:32.492708 |

Four distinct prices across the run — the interval is fast enough to catch intraday movement as it happens.

## How it works

The core of the scrape is two `find` calls against the parsed page:

```python
crypto_name  = soup.find("span", title="Bitcoin").text.replace("price", "")
crypto_price = soup.find("span", class_="sc-d1ede7e3-0 fsQm base-text").text.replace("$", "")
```

Each reading becomes a one-row DataFrame, and the write path branches on whether the file already exists:

```python
if os.path.exists(path):
    df.to_csv(path, mode="a", header=False, index=False)   # append to history
else:
    df.to_csv(path, index=False)                           # create with headers
```

That branch is what makes the dataset cumulative — restarting the script extends the history rather than wiping it.

## Tech stack

| Tool | Role |
|------|------|
| **Python** | Core language |
| **Requests** | Fetches the raw HTML from CoinMarketCap |
| **BeautifulSoup** | Parses the HTML and locates the price elements |
| **Pandas** | Structures each reading and handles the CSV read/append |
| **datetime / os / time** | Timestamping, file checks, and the polling interval |

## Running it yourself

```bash
pip install requests beautifulsoup4 pandas
python "Crypto Web Scraper.py"
```

The script loops until you stop it with `Ctrl+C`. Before running, update the CSV output path near the bottom of the file to a location on your own machine.

## Known limitations

Worth being upfront about, since these are the things I'd fix in a v2:

- **Hardcoded output path.** The CSV destination is an absolute path to my Desktop; it should be a relative path or a command-line argument.
- **Brittle price selector.** The price is found via an auto-generated CSS class (`sc-d1ede7e3-0 fsQm base-text`). CoinMarketCap regenerates these on redeploys, so the selector will eventually break.
- **No error handling.** A failed request, a rate limit, or a changed page layout will raise and kill the loop instead of retrying and moving on.
- **Minor data cleanliness.** The scraped name carries a trailing non-breaking space, and the price is stored as a comma-formatted string rather than a number.
- **Single coin.** The URL is fixed to Bitcoin rather than parameterized across tickers.

## Next steps

- Pull the coin, interval, and output path out into a config or CLI flags
- Swap the fragile class selector for CoinMarketCap's public API
- Wrap the request in `try/except` with retry and backoff so a single failure doesn't end the run
- Store prices as floats and parse timestamps on write, so the CSV is analysis-ready without cleanup
- Chart the collected history to visualize price movement over longer collection windows
