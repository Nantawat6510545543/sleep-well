from textblob import TextBlob


def analyze_opinions(comments_list):
    sentiments = [TextBlob(comment).sentiment.polarity for comment in
                  comments_list]
    average_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    return {'average_sentiment': average_sentiment,
            'total_comments': len(comments_list)}


def get_sentiments(comment):
    """
    >>> get_sentiments("I love this product!")
    0.5
    >>> get_sentiments("This movie is terrible.")
    -1.0
    >>> get_sentiments("The weather is nice today.")
    0.6
    """
    sentiments = TextBlob(comment).sentiment.polarity
    return sentiments
