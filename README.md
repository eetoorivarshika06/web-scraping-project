# Web Scraping Project — books.toscrape.com

## Project Overview

This project scrapes the full [books.toscrape.com](https://books.toscrape.com) catalog—a sandbox site built for learning web scraping. The scraper walks all **50 catalog pages** (20 books per page) and collects structured data for **1,000 books** in total.

Each record includes:

| Field | Description |
|-------|-------------|
| `title` | Book title |
| `price` | Listed price (GBP, e.g. `£51.77`) |
| `rating` | Star rating as an integer from **1 to 5** |
| `availability` | Stock status (e.g. `In stock`) |

Output is saved to **`books_dataset.csv`** for analysis or downstream use.

## Tools Used

- **Python 3** — scripting language
- **[Requests](https://requests.readthedocs.io/)** — HTTP client for fetching catalog pages
- **[Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)** — HTML parsing and extraction
- **`csv`** (stdlib) — writing the dataset
- **`time`** (stdlib) — polite delay between page requests

The scraper uses a persistent `requests.Session`, a custom `User-Agent` header, and a **1 second delay** between pages to avoid hammering the server.

## How to Run

1. **Clone or open** this project directory.

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   ```

   Activate it:

   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the scraper**:

   ```bash
   python scrape_books.py
   ```

   Progress is printed for each page, for example:

   ```
   Page 1/50: scraped 20 books (total so far: 20)
   Page 2/50: scraped 20 books (total so far: 40)
   ...
   ```

5. **Output**: `books_dataset.csv` is written in the project root when the run completes (~50 seconds of delays plus fetch time).

## Sample Insights from the Data

Analysis of the scraped `books_dataset.csv`:

1. **Every book is in stock** — All 1,000 rows show `In stock`. The demo site does not model out-of-stock items on the main catalog pages, so availability is uniform in this dataset.

2. **Prices cluster in a narrow band** — After parsing GBP values, the average price is about **£35.07**, with a low of **£10.00** (*An Abundance of Katherines*) and a high of **£59.99** (*The Perfect Play (Play by Play #1)*). The site generates prices in a tight range rather than a long tail.

3. **Ratings are spread across all five levels** — Counts by star rating are fairly balanced: 226 (1★), 196 (2★), 203 (3★), 179 (4★), and 196 (5★). The median rating is **3 stars**, with no single rating dominating the catalog.

## Project Structure

```
web_scraping_project/
├── scrape_books.py      # Main scraper script
├── books_dataset.csv    # Scraped output (generated)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Notes

- [books.toscrape.com](https://books.toscrape.com) is intended for practice; respect its terms and use reasonable request rates.
- Re-running `scrape_books.py` overwrites `books_dataset.csv`.
