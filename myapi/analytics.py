from textblob import TextBlob


def analyze_opinions(comments_list):
    sentiments = [TextBlob(comment).sentiment.polarity for comment in
                  comments_list]
    average_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    return {'average_sentiment': average_sentiment,
            'total_comments': len(comments_list)}
