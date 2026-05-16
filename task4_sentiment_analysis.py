"""Sentiment analysis on book catalog and sample product reviews."""

import re
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

BOOKS_CSV = "books_dataset.csv"
REVIEWS_CSV = "reviews_dataset.csv"
SUMMARY_TXT = "sentiment_summary.txt"
ACCENT = "#f97316"
DPI = 150

# 50 hardcoded Amazon-style reviews (books, electronics, food)
SAMPLE_REVIEWS = [
    {"category": "books", "product": "Mystery Thriller", "star_rating": 5,
     "review_text": "Absolutely gripping from page one! Could not put it down, finished in two days with pure joy."},
    {"category": "books", "product": "Cookbook Collection", "star_rating": 4,
     "review_text": "Great recipes and beautiful photos. A few dishes were disappointing but overall very helpful."},
    {"category": "books", "product": "Self-Help Guide", "star_rating": 2,
     "review_text": "Repetitive advice and boring chapters. I regret buying this waste of money."},
    {"category": "books", "product": "Fantasy Epic", "star_rating": 5,
     "review_text": "Magical world-building and lovable characters. This book made me laugh and cry with happiness."},
    {"category": "books", "product": "History Textbook", "star_rating": 3,
     "review_text": "Informative but dry. Decent reference material, nothing exciting here."},
    {"category": "books", "product": "Romance Novel", "star_rating": 1,
     "review_text": "Terrible plot and awful dialogue. Angry that I spent time on this disaster."},
    {"category": "books", "product": "Science Fiction", "star_rating": 5,
     "review_text": "Mind-blowing twists and brilliant ideas. Surprised by how good the ending was!"},
    {"category": "books", "product": "Poetry Anthology", "star_rating": 4,
     "review_text": "Touching and thoughtful poems. Some feel sad but beautifully written."},
    {"category": "books", "product": "Biography", "star_rating": 3,
     "review_text": "Okay read. Learned a few things but pacing was slow in the middle."},
    {"category": "books", "product": "Children's Storybook", "star_rating": 5,
     "review_text": "My kids adore this! Fun illustrations and delightful stories every night."},
    {"category": "books", "product": "Business Strategy", "star_rating": 2,
     "review_text": "Outdated examples and vague tips. Fear this won't help my career at all."},
    {"category": "books", "product": "Graphic Novel", "star_rating": 4,
     "review_text": "Stunning artwork and solid story. Really enjoyed the action scenes."},
    {"category": "books", "product": "Travel Guide", "star_rating": 3,
     "review_text": "Useful maps but missing recent spots. Neutral experience overall."},
    {"category": "books", "product": "Horror Collection", "star_rating": 5,
     "review_text": "Genuinely scary! I was afraid to read at night but loved every moment."},
    {"category": "books", "product": "Classic Literature", "star_rating": 4,
     "review_text": "Timeless prose and deep themes. Happy to finally read this masterpiece."},
    {"category": "books", "product": "Study Guide", "star_rating": 1,
     "review_text": "Full of errors and confusing explanations. Furious about this purchase."},
    {"category": "books", "product": "Art Book", "star_rating": 5,
     "review_text": "Gorgeous prints and inspiring commentary. Pure joy for any art lover."},
    {"category": "electronics", "product": "Wireless Earbuds", "star_rating": 5,
     "review_text": "Crystal clear sound and comfortable fit. Best earbuds I have ever owned!"},
    {"category": "electronics", "product": "Budget Smartphone", "star_rating": 2,
     "review_text": "Slow performance and terrible battery. Disappointed and annoyed daily."},
    {"category": "electronics", "product": "4K Monitor", "star_rating": 4,
     "review_text": "Sharp display and easy setup. Great for work, minor backlight bleed."},
    {"category": "electronics", "product": "Gaming Laptop", "star_rating": 5,
     "review_text": "Runs every game smoothly! Thrilled with the speed and RGB keyboard."},
    {"category": "electronics", "product": "Bluetooth Speaker", "star_rating": 3,
     "review_text": "Decent bass for the price. Nothing special, acceptable for parties."},
    {"category": "electronics", "product": "Smart Watch", "star_rating": 4,
     "review_text": "Accurate fitness tracking and sleek design. Happy with daily use."},
    {"category": "electronics", "product": "USB-C Hub", "star_rating": 1,
     "review_text": "Stopped working after a week. Angry about the cheap build quality."},
    {"category": "electronics", "product": "Mechanical Keyboard", "star_rating": 5,
     "review_text": "Satisfying clicks and premium feel. Typing is a joy on this board."},
    {"category": "electronics", "product": "Webcam HD", "star_rating": 2,
     "review_text": "Grainy video and poor low-light performance. Sad about video calls."},
    {"category": "electronics", "product": "Tablet 10-inch", "star_rating": 4,
     "review_text": "Bright screen and long battery. Surprised how good it is for reading."},
    {"category": "electronics", "product": "Noise Cancelling Headphones", "star_rating": 5,
     "review_text": "Blocks out everything! Peaceful flights and happy commuting."},
    {"category": "electronics", "product": "Smart Thermostat", "star_rating": 4,
     "review_text": "Saved money on heating bills. Easy app, slight fear of setup at first."},
    {"category": "electronics", "product": "Drone Mini", "star_rating": 5,
     "review_text": "Amazing aerial shots and stable flight. Delighted with every flight!"},
    {"category": "electronics", "product": "Router Wi-Fi 6", "star_rating": 2,
     "review_text": "Frequent drops and confusing interface. Frustrated with connectivity."},
    {"category": "electronics", "product": "Fitness Tracker Band", "star_rating": 4,
     "review_text": "Lightweight and accurate steps. Good value, comfortable strap."},
    {"category": "electronics", "product": "External SSD 1TB", "star_rating": 5,
     "review_text": "Blazing fast transfers! Ecstatic about backup speeds."},
    {"category": "electronics", "product": "Action Camera", "star_rating": 1,
     "review_text": "Footage was shaky and audio terrible. Worst purchase this year."},
    {"category": "food", "product": "Organic Coffee Beans", "star_rating": 5,
     "review_text": "Rich aroma and smooth taste every morning. Pure joy in a cup!"},
    {"category": "food", "product": "Protein Bar Variety", "star_rating": 3,
     "review_text": "Some flavors good, others chalky. Okay snack, nothing amazing."},
    {"category": "food", "product": "Hot Sauce Gift Set", "star_rating": 4,
     "review_text": "Spicy and flavorful! Surprised by the smoky chipotle one."},
    {"category": "food", "product": "Frozen Pizza Pack", "star_rating": 2,
     "review_text": "Soggy crust and bland cheese. Disappointed with every slice."},
    {"category": "food", "product": "Dark Chocolate Box", "star_rating": 5,
     "review_text": "Luxurious and delicious. Happy to gift these to friends."},
    {"category": "food", "product": "Instant Ramen Bulk", "star_rating": 4,
     "review_text": "Quick and tasty for late nights. Great comfort food."},
    {"category": "food", "product": "Almond Butter Jar", "star_rating": 3,
     "review_text": "Creamy but separates quickly. Neutral on repurchasing."},
    {"category": "food", "product": "Green Tea Matcha", "star_rating": 5,
     "review_text": "Vibrant color and calming ritual. Delighted with the quality."},
    {"category": "food", "product": "Beef Jerky Sampler", "star_rating": 2,
     "review_text": "Too salty and tough. Angry about the small portions."},
    {"category": "food", "product": "Granola Cereal", "star_rating": 4,
     "review_text": "Crunchy clusters and real fruit. Enjoy breakfast again."},
    {"category": "food", "product": "Olive Oil Extra Virgin", "star_rating": 5,
     "review_text": "Fruity and fresh on salads. Thrilled with this kitchen staple."},
    {"category": "food", "product": "Meal Kit Delivery", "star_rating": 1,
     "review_text": "Arrived warm and ingredients wilted. Furious about wasted money."},
    {"category": "food", "product": "Sparkling Water Case", "star_rating": 3,
     "review_text": "Refreshing but plain. Fine for hydration, no excitement."},
    {"category": "food", "product": "Honey Raw Organic", "star_rating": 5,
     "review_text": "Sweet and floral flavor. Joy spreading it on warm toast."},
    {"category": "food", "product": "Vegan Cheese Block", "star_rating": 2,
     "review_text": "Strange aftertaste and won't melt. Sad attempt at cheese."},
    {"category": "food", "product": "Sourdough Bread Mix", "star_rating": 5,
     "review_text": "Perfect crust and tangy flavor! Ecstatic home baker here."},
]

EMOTION_KEYWORDS = {
    "joy": [
        "joy", "happy", "delight", "love", "ecstatic", "thrilled", "glad",
        "wonderful", "best", "adorable", "pleased", "enjoy", "brilliant",
    ],
    "anger": [
        "angry", "furious", "annoyed", "frustrated", "terrible", "awful",
        "worst", "waste", "disaster", "regret", "cheap",
    ],
    "fear": [
        "fear", "afraid", "scary", "worried", "anxious", "terrified", "dread",
    ],
    "surprise": [
        "surprise", "surprised", "shocked", "unexpected", "mind-blowing", "amazing",
    ],
    "sadness": [
        "sad", "disappointed", "boring", "dry", "slow", "unhappy", "cry", "regret",
    ],
}


def apply_dark_theme() -> None:
    plt.style.use("dark_background")
    sns.set_theme(
        style="darkgrid",
        rc={"axes.facecolor": "#1a1a1a", "figure.facecolor": "#0d0d0d"},
    )


def vader_label(compound: float) -> str:
    if compound >= 0.05:
        return "Positive"
    if compound <= -0.05:
        return "Negative"
    return "Neutral"


def detect_emotion(text: str) -> str:
    words = set(re.findall(r"[a-z']+", text.lower()))
    scores = {
        emotion: sum(1 for kw in keywords if kw in words)
        for emotion, keywords in EMOTION_KEYWORDS.items()
    }
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "neutral"


def build_reviews_dataset() -> pd.DataFrame:
    reviews = pd.DataFrame(SAMPLE_REVIEWS)
    reviews.insert(0, "review_id", range(1, len(reviews) + 1))
    return reviews


def analyze_reviews(reviews: pd.DataFrame) -> pd.DataFrame:
    analyzer = SentimentIntensityAnalyzer()
    rows = []

    for _, row in reviews.iterrows():
        text = row["review_text"]
        vader = analyzer.polarity_scores(text)
        blob = TextBlob(text)

        rows.append(
            {
                **row.to_dict(),
                "vader_compound": round(vader["compound"], 4),
                "vader_positive": round(vader["pos"], 4),
                "vader_negative": round(vader["neg"], 4),
                "vader_neutral": round(vader["neu"], 4),
                "vader_sentiment": vader_label(vader["compound"]),
                "textblob_polarity": round(blob.sentiment.polarity, 4),
                "textblob_subjectivity": round(blob.sentiment.subjectivity, 4),
                "dominant_emotion": detect_emotion(text),
            }
        )

    return pd.DataFrame(rows)


def load_books_summary() -> pd.DataFrame:
    books = pd.read_csv(BOOKS_CSV)
    books["price"] = (
        books["price"].astype(str).str.replace(r"[^\d.]", "", regex=True).astype(float)
    )
    books["rating"] = pd.to_numeric(books["rating"], errors="coerce")
    return books


def rating_sentiment_correlation(df: pd.DataFrame) -> float:
    return df["star_rating"].corr(df["vader_compound"])


def write_summary(df: pd.DataFrame, books: pd.DataFrame, correlation: float) -> str:
    sentiment_counts = df["vader_sentiment"].value_counts()
    emotion_counts = df["dominant_emotion"].value_counts()
    avg_by_rating = df.groupby("star_rating")["vader_compound"].mean()

    lines = [
        "SENTIMENT ANALYSIS SUMMARY",
        "=" * 40,
        f"Total reviews analyzed: {len(df)}",
        f"Books in catalog (reference): {len(books)}",
        "",
        "VADER sentiment distribution:",
        *[f"  {k}: {v}" for k, v in sentiment_counts.items()],
        "",
        f"Rating vs sentiment correlation: {correlation:.3f}",
        f"Most common emotion: {emotion_counts.idxmax()} ({emotion_counts.max()} reviews)",
        f"Average TextBlob polarity: {df['textblob_polarity'].mean():.3f}",
        f"Average TextBlob subjectivity: {df['textblob_subjectivity'].mean():.3f}",
        "",
        "Average VADER compound score by star rating:",
        *[f"  {int(r)} stars: {s:.3f}" for r, s in avg_by_rating.items()],
        "",
        "Category breakdown:",
    ]
    for cat, grp in df.groupby("category"):
        pos_pct = (grp["vader_sentiment"] == "Positive").mean() * 100
        lines.append(f"  {cat}: {len(grp)} reviews, {pos_pct:.0f}% positive")

    lines.extend([
        "",
        "Key insight: Higher star ratings generally align with more positive",
        "VADER compound scores, confirming review text matches assigned ratings.",
    ])
    text = "\n".join(lines)
    with open(SUMMARY_TXT, "w", encoding="utf-8") as f:
        f.write(text)
    return text


def chart_sentiment_distribution(df: pd.DataFrame) -> None:
    counts = df["vader_sentiment"].value_counts().reindex(
        ["Positive", "Neutral", "Negative"]
    ).fillna(0)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.bar(counts.index, counts.values, color=ACCENT, edgecolor="white", linewidth=0.6)
    ax.bar_label(bars, padding=4, color="white")
    ax.set_title("Sentiment Distribution (VADER)", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Number of reviews")
    ax.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig("chart_task4_sentiment_distribution.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close()


def chart_polarity_subjectivity(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 5.5))
    scatter = ax.scatter(
        df["textblob_polarity"],
        df["textblob_subjectivity"],
        c=df["star_rating"],
        cmap="Oranges",
        s=80,
        alpha=0.85,
        edgecolors="white",
        linewidths=0.4,
    )
    ax.set_title("TextBlob Polarity vs Subjectivity", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Polarity")
    ax.set_ylabel("Subjectivity")
    ax.axvline(0, color="#64748b", linestyle="--", linewidth=0.8)
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Star rating")
    ax.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig("chart_task4_polarity_subjectivity.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close()


def chart_sentiment_by_rating(df: pd.DataFrame) -> None:
    avg = df.groupby("star_rating")["vader_compound"].mean().sort_index()

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.bar(avg.index.astype(str), avg.values, color=ACCENT, edgecolor="white", linewidth=0.6)
    ax.bar_label(bars, fmt="%.2f", padding=4, color="white")
    ax.set_title("Average Sentiment Score per Star Rating", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Star rating")
    ax.set_ylabel("Average VADER compound")
    ax.axhline(0, color="#64748b", linestyle="--", linewidth=0.8)
    ax.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig("chart_task4_sentiment_by_rating.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close()


def chart_emotion_distribution(df: pd.DataFrame) -> None:
    counts = df["dominant_emotion"].value_counts().sort_values()

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.barh(counts.index, counts.values, color=ACCENT, edgecolor="white", linewidth=0.6)
    ax.bar_label(bars, padding=4, color="white")
    ax.set_title("Emotion Distribution (NRC-style keywords)", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Number of reviews")
    ax.grid(axis="x", alpha=0.25)
    plt.tight_layout()
    plt.savefig("chart_task4_emotion_distribution.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close()


def chart_sentiment_pie(df: pd.DataFrame) -> None:
    counts = df["vader_sentiment"].value_counts()
    colors = [ACCENT if label == "Positive" else "#334155" for label in counts.index]

    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        explode=[0.03] * len(counts),
        wedgeprops={"edgecolor": "#0d0d0d", "linewidth": 1.2},
        textprops={"color": "white", "fontsize": 11},
    )
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")
    ax.set_title("Overall Sentiment Split", fontsize=14, fontweight="bold", pad=16)
    plt.tight_layout()
    plt.savefig("chart_task4_sentiment_pie.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close()


def print_summary_table(df: pd.DataFrame) -> None:
    cols = [
        "review_id", "category", "star_rating", "vader_sentiment",
        "vader_compound", "textblob_polarity", "textblob_subjectivity", "dominant_emotion",
    ]
    print("\n=== REVIEW SENTIMENT SUMMARY TABLE ===")
    print(df[cols].to_string(index=False))
    print(f"\nTotal reviews: {len(df)}")


def main() -> None:
    apply_dark_theme()

    books = load_books_summary()
    print(f"Loaded {len(books)} books from {BOOKS_CSV}")

    reviews = build_reviews_dataset()
    analyzed = analyze_reviews(reviews)
    analyzed.to_csv(REVIEWS_CSV, index=False)
    print(f"Saved {len(analyzed)} reviews to {REVIEWS_CSV}")

    correlation = rating_sentiment_correlation(analyzed)
    summary = write_summary(analyzed, books, correlation)
    print(f"Saved insights to {SUMMARY_TXT}")

    chart_sentiment_distribution(analyzed)
    chart_polarity_subjectivity(analyzed)
    chart_sentiment_by_rating(analyzed)
    chart_emotion_distribution(analyzed)
    chart_sentiment_pie(analyzed)
    print("Saved 5 charts: chart_task4_*.png")

    print_summary_table(analyzed)
    print("\n=== SUMMARY INSIGHTS ===")
    print(summary)


if __name__ == "__main__":
    main()
