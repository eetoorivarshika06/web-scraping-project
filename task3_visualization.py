"""Publication-quality visualizations for books_dataset.csv."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

CSV_FILE = "books_dataset.csv"
ACCENT = "#f97316"
DPI = 150


def load_and_prepare(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["price"] = (
        df["price"].astype(str).str.replace(r"[^\d.]", "", regex=True).astype(float)
    )
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["in_stock"] = df["availability"].str.strip().str.lower() == "in stock"
    df["availability_num"] = df["in_stock"].astype(int)
    return df


def apply_dark_theme() -> None:
    plt.style.use("dark_background")
    sns.set_theme(style="darkgrid", rc={"axes.facecolor": "#1a1a1a", "figure.facecolor": "#0d0d0d"})


def chart_avg_price_by_rating(df: pd.DataFrame) -> None:
    avg_by_rating = df.groupby("rating")["price"].mean().sort_index()

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.bar(
        avg_by_rating.index.astype(str),
        avg_by_rating.values,
        color=ACCENT,
        edgecolor="white",
        linewidth=0.6,
    )
    ax.bar_label(bars, fmt="£%.2f", padding=4, fontsize=9, color="white")

    ax.set_title("Average Price by Star Rating", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Star rating", fontsize=11)
    ax.set_ylabel("Average price (£)", fontsize=11)
    ax.set_ylim(0, avg_by_rating.max() * 1.15)
    ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()
    plt.savefig("chart_task3_avg_price_by_rating.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close()
    print("Saved: chart_task3_avg_price_by_rating.png")


def chart_price_histogram(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.hist(
        df["price"],
        bins=30,
        color=ACCENT,
        edgecolor="#0d0d0d",
        linewidth=0.8,
        alpha=0.9,
    )
    ax.axvline(df["price"].mean(), color="white", linestyle="--", linewidth=1.2, label=f"Mean: £{df['price'].mean():.2f}")
    ax.axvline(df["price"].median(), color="#94a3b8", linestyle=":", linewidth=1.2, label=f"Median: £{df['price'].median():.2f}")

    ax.set_title("Price Distribution Across All Books", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Price (£)", fontsize=11)
    ax.set_ylabel("Number of books", fontsize=11)
    ax.legend(frameon=True, facecolor="#1a1a1a", edgecolor="#333333")
    ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()
    plt.savefig("chart_task3_price_histogram.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close()
    print("Saved: chart_task3_price_histogram.png")


def chart_stock_pie(df: pd.DataFrame) -> None:
    stock_counts = df["in_stock"].value_counts()
    labels = ["In stock" if idx else "Out of stock" for idx in stock_counts.index]
    colors = [ACCENT if label == "In stock" else "#334155" for label in labels]

    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        stock_counts.values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        explode=[0.03] * len(stock_counts),
        wedgeprops={"edgecolor": "#0d0d0d", "linewidth": 1.2},
        textprops={"color": "white", "fontsize": 11},
    )
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")

    ax.set_title("In Stock vs Out of Stock", fontsize=14, fontweight="bold", pad=16)

    plt.tight_layout()
    plt.savefig("chart_task3_stock_pie.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close()
    print("Saved: chart_task3_stock_pie.png")


def chart_correlation_heatmap(df: pd.DataFrame) -> None:
    numeric = df[["price", "rating", "availability_num"]].rename(
        columns={"availability_num": "availability"}
    )
    corr = numeric.corr()

    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="Oranges",
        vmin=-1,
        vmax=1,
        linewidths=0.8,
        linecolor="#0d0d0d",
        cbar_kws={"label": "Correlation"},
        ax=ax,
    )
    ax.set_title(
        "Correlation: Price, Rating & Availability",
        fontsize=14,
        fontweight="bold",
        pad=12,
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

    plt.tight_layout()
    plt.savefig("chart_task3_correlation_heatmap.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close()
    print("Saved: chart_task3_correlation_heatmap.png")


def chart_price_boxplot(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 5.5))
    sns.boxplot(
        data=df,
        x="rating",
        y="price",
        color=ACCENT,
        width=0.55,
        fliersize=3,
        boxprops={"edgecolor": "white", "linewidth": 1},
        medianprops={"color": "white", "linewidth": 1.5},
        whiskerprops={"color": ACCENT},
        capprops={"color": ACCENT},
        ax=ax,
    )
    sns.stripplot(
        data=df,
        x="rating",
        y="price",
        color="white",
        alpha=0.15,
        size=2,
        jitter=0.25,
        ax=ax,
    )

    ax.set_title("Price Spread per Rating Category", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Star rating", fontsize=11)
    ax.set_ylabel("Price (£)", fontsize=11)
    ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()
    plt.savefig("chart_task3_price_boxplot.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close()
    print("Saved: chart_task3_price_boxplot.png")


def main() -> None:
    apply_dark_theme()
    df = load_and_prepare(CSV_FILE)
    print(f"Loaded {len(df)} books from {CSV_FILE}\n")

    chart_avg_price_by_rating(df)
    chart_price_histogram(df)
    chart_stock_pie(df)
    chart_correlation_heatmap(df)
    chart_price_boxplot(df)

    print("\nAll Task 3 charts saved.")


if __name__ == "__main__":
    main()
