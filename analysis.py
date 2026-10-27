"""Pandas analysis module: generates summary statistics and Chart.js payloads."""
import pandas as pd


def summary(df):
    if df.empty:
        return None
    return {
        "total": len(df),
        "avg_price": round(df["price"].mean(), 2),
        "median_price": round(df["price"].median(), 2),
        "min_price": df["price"].min(),
        "max_price": df["price"].max(),
        "avg_rating": round(df["rating"].mean(), 2),
        "in_stock_pct": round(df["in_stock"].mean() * 100, 1),
    }


def chart_data(df):
    if df.empty:
        return {}

    counts = df["rating"].value_counts().sort_index()
    avg_price = df.groupby("rating")["price"].mean().round(2)

    buckets = pd.cut(
        df["price"],
        bins=[0, 20, 30, 40, 50, 100],
        labels=["Under £20", "£20-30", "£30-40", "£40-50", "£50+"],
    ).value_counts().sort_index()

    return {
        "rating_labels": [f"{int(k)} Stars" for k in counts.index],
        "rating_counts": [int(v) for v in counts.values],
        "price_labels": [f"{int(k)} Stars" for k in avg_price.index],
        "price_values": [float(v) for v in avg_price.values],
        "bucket_labels": [str(k) for k in buckets.index],
        "bucket_counts": [int(v) for v in buckets.values],
    }


def top_expensive(df, n=5):
    return df.nlargest(n, "price")[["title", "price", "rating"]].to_dict("records")