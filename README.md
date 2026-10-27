# 📚 Book Analytics & Scraper Web App

A Flask web application that scrapes book data from [books.toscrape.com](https://books.toscrape.com), stores records inside a local SQLite database, performs statistical breakdowns using Pandas, and visualizes trends using Chart.js.

## 🚀 Features

- **Automated Web Scraping**: Fetches titles, prices, ratings, availability, and thumbnails using BeautifulSoup and Requests.
- **SQLite Persistence**: Stores and deduplicates entries using SQLite `ON CONFLICT` updates.
- **Data Analytics**: Computes aggregate metrics (averages, medians, price distribution buckets) via Pandas.
- **Interactive UI & Charts**: Built with Bootstrap 5 (dark/light mode toggle) and Chart.js graphs.
- **Pagination & Filtering**: Search by title, filter by rating/stock, and sort by price or rating.

## 🛠️ Tech Stack

- **Backend**: Python, Flask, SQLite3
- **Scraping & Data Processing**: Requests, BeautifulSoup4, Pandas
- **Frontend**: HTML5, Jinja2, Bootstrap 5, Chart.js

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/](https://github.com/)<YOUR-USERNAME>/<YOUR-REPO-NAME>.git
   cd <YOUR-REPO-NAME>
