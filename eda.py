"""Exploratory data analysis for books_dataset.csv."""

import matplotlib.pyplot as plt
import pandas as pd

CSV_FILE = "books_dataset.csv"


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def clean_price(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.replace(r"[^\d.]", "", regex=True)
        .astype(float)
    )


def main() -> None:
    # ------------------------------------------------------------------
    # 1. Load and inspect
    # ------------------------------------------------------------------
    section("LOAD AND INSPECT")
    df = pd.read_csv(CSV_FILE)
    print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"\nColumn names:\n{list(df.columns)}")
    print(f"\nData types:\n{df.dtypes}")
    print(f"\nFirst 5 rows:\n{df.head()}")

    # ------------------------------------------------------------------
    # 2. Clean data
    # ------------------------------------------------------------------
    section("CLEAN DATA")
    df["price"] = clean_price(df["price"])
    df["availability"] = df["availability"].str.strip().str.lower() == "in stock"
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    print("Price converted to float (currency symbols removed).")
    print("Availability converted to boolean (True = In stock).")
    print(df[["title", "price", "rating", "availability"]].head())

    # ------------------------------------------------------------------
    # 3. Feature engineering
    # ------------------------------------------------------------------
    section("NEW COLUMNS")
    df["price_range"] = pd.cut(
        df["price"],
        bins=[-float("inf"), 20, 40, float("inf")],
        labels=["Cheap", "Mid", "Expensive"],
    )
    df["in_stock"] = df["availability"]
    df["value_score"] = (df["rating"] / df["price"]).round(2)
    print(
        df[["title", "price", "rating", "price_range", "in_stock", "value_score"]].head()
    )

    # ------------------------------------------------------------------
    # 4. Basic statistics
    # ------------------------------------------------------------------
    section("BASIC STATISTICS")
    mean_price = df["price"].mean()
    median_price = df["price"].median()
    most_common_rating = int(df["rating"].mode().iloc[0])
    pct_in_stock = df["in_stock"].mean() * 100

    print(f"Mean price:   £{mean_price:.2f}")
    print(f"Median price: £{median_price:.2f}")
    print(f"Most common rating: {most_common_rating} stars")
    print(f"Books in stock: {pct_in_stock:.1f}%")

    # ------------------------------------------------------------------
    # 5. Questions
    # ------------------------------------------------------------------
    section("QUESTIONS")

    avg_price_by_rating = df.groupby("rating")["price"].mean()
    highest_avg_rating = int(avg_price_by_rating.idxmax())
    print(
        f"Rating with highest average price: {highest_avg_rating} stars "
        f"(£{avg_price_by_rating.max():.2f})"
    )

    price_range_counts = df["price_range"].value_counts()
    most_common_range = price_range_counts.idxmax()
    print(
        f"Price range with most books: {most_common_range} "
        f"({price_range_counts.max()} books)"
    )

    expensive = df[df["price_range"] == "Expensive"]
    if len(expensive) > 0:
        expensive_in_stock_pct = expensive["in_stock"].mean() * 100
    else:
        expensive_in_stock_pct = 0.0
    print(f"% of expensive books in stock: {expensive_in_stock_pct:.1f}%")

    top_value = df.nlargest(5, "value_score")[["title", "price", "rating", "value_score"]]
    print("\nTop 5 best value books (highest value_score):")
    print(top_value.to_string(index=False))

    # ------------------------------------------------------------------
    # 6. Anomalies
    # ------------------------------------------------------------------
    section("ANOMALY DETECTION")

    zero_price = df[df["price"] == 0]
    print(f"Books with price 0: {len(zero_price)}")
    if len(zero_price) > 0:
        print(zero_price[["title", "price"]].to_string(index=False))

    duplicate_titles = df[df.duplicated(subset=["title"], keep=False)]
    n_dup_titles = df["title"].duplicated().sum()
    print(f"\nDuplicate titles: {n_dup_titles}")
    if n_dup_titles > 0:
        print(
            duplicate_titles.sort_values("title")[["title", "price", "rating"]].head(10)
        )

    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]
    if missing_cols.empty:
        print("\nMissing values: none")
    else:
        print("\nMissing values by column:")
        print(missing_cols)

    # ------------------------------------------------------------------
    # 7. Charts
    # ------------------------------------------------------------------
    section("CHARTS")

    # Bar chart: average price by rating
    rating_price = df.groupby("rating")["price"].mean().sort_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    rating_price.plot(kind="bar", ax=ax, color="steelblue", edgecolor="black")
    ax.set_title("Average Price by Rating")
    ax.set_xlabel("Rating (stars)")
    ax.set_ylabel("Average price (£)")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    plt.tight_layout()
    plt.savefig("chart_avg_price_by_rating.png", dpi=150)
    plt.close()
    print("Saved: chart_avg_price_by_rating.png")

    # Bar chart: count per price range
    range_counts = df["price_range"].value_counts().reindex(
        ["Cheap", "Mid", "Expensive"]
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    range_counts.plot(kind="bar", ax=ax, color="coral", edgecolor="black")
    ax.set_title("Number of Books per Price Range")
    ax.set_xlabel("Price range")
    ax.set_ylabel("Count")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    plt.tight_layout()
    plt.savefig("chart_books_per_price_range.png", dpi=150)
    plt.close()
    print("Saved: chart_books_per_price_range.png")

    # Pie chart: in stock vs out of stock
    stock_counts = df["in_stock"].value_counts()
    labels = ["In stock" if idx else "Out of stock" for idx in stock_counts.index]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        stock_counts.values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=["#2ecc71", "#e74c3c"],
    )
    ax.set_title("In Stock vs Out of Stock")
    plt.tight_layout()
    plt.savefig("chart_stock_pie.png", dpi=150)
    plt.close()
    print("Saved: chart_stock_pie.png")

    # Scatter: price vs rating, colored by value_score
    fig, ax = plt.subplots(figsize=(9, 6))
    scatter = ax.scatter(
        df["price"],
        df["rating"],
        c=df["value_score"],
        cmap="viridis",
        alpha=0.7,
        edgecolors="none",
    )
    ax.set_title("Price vs Rating (colored by value_score)")
    ax.set_xlabel("Price (£)")
    ax.set_ylabel("Rating (stars)")
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("value_score")
    plt.tight_layout()
    plt.savefig("chart_price_vs_rating.png", dpi=150)
    plt.close()
    print("Saved: chart_price_vs_rating.png")

    section("DONE")
    print("EDA complete.")


if __name__ == "__main__":
    main()
