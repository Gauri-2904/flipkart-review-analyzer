import streamlit as st
import pandas as pd

st.title("🛒 Flipkart Customer Review Analyzer")

# Upload CSV
uploaded_file = st.file_uploader("Upload your dataset", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader(" Dataset Preview")
    st.dataframe(df.head())

    st.write("Columns:", df.columns)

    # Select column
    column = st.selectbox("Select Review Column", df.columns)

    # Remove NaN values from selected column
    df = df.dropna(subset=[column])

    # -----------------------------
    # Stopwords list
    # -----------------------------
    stopwords = [
        "the", "is", "and", "a", "to", "of", "in", "for", "on", "with",
        "this", "that", "it", "not", "was", "are", "as", "but"
    ]

    # -----------------------------
    # Word Frequency Function
    # -----------------------------
    def count_word_frequency(text_list):
        word_count = {}

        for text in text_list:
            words = str(text).split()

            for word in words:
                word = word.lower().strip('.,!?";:')

                if word and word not in stopwords:
                    word_count[word] = word_count.get(word, 0) + 1

        return word_count

    result = count_word_frequency(df[column])

    sorted_words = sorted(result.items(), key=lambda x: x[1], reverse=True)

    # -----------------------------
    # Top Words
    # -----------------------------
    st.subheader("🔥 Top 10 Frequent Words")
    for word, count in sorted_words[:10]:
        st.write(f"{word} : {count}")

    st.bar_chart(dict(sorted_words[:10]))

    # -----------------------------
    # Word-based Sentiment
    # -----------------------------
    positive_words = ["good", "great", "awesome", "excellent", "nice", "amazing", "love"]
    negative_words = ["bad", "worst", "poor", "slow", "hate", "terrible"]

    pos = 0
    neg = 0

    for word, count in result.items():
        if word in positive_words:
            pos += count
        elif word in negative_words:
            neg += count

    st.subheader("😊 Word Sentiment Analysis")
    st.write(f"Positive Words: {pos}")
    st.write(f"Negative Words: {neg}")

    st.bar_chart({
        "Positive": pos,
        "Negative": neg
    })

    # -----------------------------
    # Rating-based Sentiment (FIXED 🔥)
    # -----------------------------
    if 'Rate' in df.columns:

        # Convert to numeric (IMPORTANT FIX)
        df['Rate'] = pd.to_numeric(df['Rate'], errors='coerce')

        # Remove invalid values
        df = df.dropna(subset=['Rate'])

        positive_r = df[df['Rate'] >= 4].shape[0]
        negative_r = df[df['Rate'] <= 2].shape[0]
        neutral_r = df[df['Rate'] == 3].shape[0]

        st.subheader("⭐ Rating-Based Sentiment")
        st.write(f"Positive Reviews 😊: {positive_r}")
        st.write(f"Negative Reviews 😡: {negative_r}")
        st.write(f"Neutral Reviews 😐: {neutral_r}")

        st.bar_chart({
            "Positive": positive_r,
            "Negative": negative_r,
            "Neutral": neutral_r
        })