"""Flask web app. Run: python app.py"""
import math
import os
import time

from flask import Flask, flash, redirect, render_template, request, url_for

import analysis
import database
import scraper

PER_PAGE = 12

app = Flask(__name__)
app.secret_key = "mini-project-secret-key"


@app.route("/")
def dashboard():
    df = database.load_books()
    stats = analysis.summary(df)
    chart_info = analysis.chart_data(df) if stats else {}
    top = analysis.top_expensive(df) if stats else []
    return render_template(
        "index.html",
        stats=stats,
        chart_info=chart_info,
        top=top,
    )


@app.route("/scrape", methods=["POST"])
def scrape():
    try:
        pages = max(1, min(int(request.form.get("pages", 1)), 50))
    except ValueError:
        flash("Please enter a valid page number (1 to 50).", "error")
        return redirect(url_for("dashboard"))

    try:
        books = scraper.scrape_books(max_pages=pages)
        new = database.save_books(books)
        flash(f"Scraped {len(books)} books ({new} newly added to database).", "ok")
    except scraper.ScrapeError as err:
        flash(f"Scraping failed: {err}", "error")
    return redirect(url_for("dashboard"))


@app.route("/books")
def books():
    df = database.load_books()
    q = request.args.get("q", "").strip()
    sort = request.args.get("sort", "default")
    rating_filter = request.args.get("rating", "")
    in_stock_only = request.args.get("in_stock", "")
    
    try:
        page = max(1, int(request.args.get("page", 1)))
    except ValueError:
        page = 1

    if not df.empty:
        df["image_url"] = df["image_url"].fillna("")

        if q:
            df = df[df["title"].str.contains(q, case=False, regex=False)]
        if rating_filter.isdigit():
            df = df[df["rating"] == int(rating_filter)]
        if in_stock_only == "1":
            df = df[df["in_stock"] == 1]

        if sort == "price_asc":
            df = df.sort_values(by="price", ascending=True)
        elif sort == "price_desc":
            df = df.sort_values(by="price", ascending=False)
        elif sort == "rating_desc":
            df = df.sort_values(by="rating", ascending=False)

    total = len(df)
    pages = max(1, math.ceil(total / PER_PAGE))
    page = min(page, pages)
    start = (page - 1) * PER_PAGE
    page_df = df.iloc[start:start + PER_PAGE]
    page_numbers = list(range(max(1, page - 2), min(pages, page + 2) + 1))
    args = {k: v for k, v in request.args.items() if k != "page"}

    return render_template(
        "books.html",
        books=page_df.to_dict("records"),
        total=total,
        page=page,
        pages=pages,
        page_numbers=page_numbers,
        args=args,
        q=q,
        sort=sort,
        rating_filter=rating_filter,
        in_stock_only=in_stock_only,
    )


@app.route("/clear", methods=["POST"])
def clear():
    database.clear_books()
    flash("Database cleared successfully.", "ok")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    database.init_db()
    app.run(debug=True)