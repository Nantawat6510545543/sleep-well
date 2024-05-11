from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def preprocessing(comment):
    # Tokenize the comment
    tokens = word_tokenize(comment.lower())  # Convert to lowercase

    # Remove punctuation and non-alphabetic characters
    tokens = [word for word in tokens if word.isalpha()]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]

    # Join tokens back into a string
    preprocessed_comment = ' '.join(tokens)

    return preprocessed_comment


def get_analytics_data(comments_list):
    if not comments_list:
        return None
    positive_comments = []
    negative_comments = []
    neutral_comments = []
    total_sentiment_score = 0

    for comment in comments_list:
        # Preprocess each comment before sentiment analysis
        preprocessed_comment = preprocessing(comment)

        # Perform sentiment analysis using TextBlob
        blob = TextBlob(preprocessed_comment)
        sentiment_score = blob.sentiment.polarity

        total_sentiment_score += sentiment_score

        # Classify comments based on sentiment score
        if sentiment_score > 0:
            positive_comments.append(comment)
        elif sentiment_score < 0:
            negative_comments.append(comment)
        else:
            neutral_comments.append(comment)

    total_comments = len(comments_list)
    positive_percentage = (len(positive_comments) / total_comments) * 100
    negative_percentage = (len(negative_comments) / total_comments) * 100
    neutral_percentage = (len(neutral_comments) / total_comments) * 100

    average_sentiment = total_sentiment_score / total_comments

    sentiment_analysis_results = {
        'total_comments': total_comments,
        # 'positive_comments': positive_comments,
        'positive_percentage': positive_percentage,
        # 'negative_comments': negative_comments,
        'negative_percentage': negative_percentage,
        # 'neutral_comments': neutral_comments,
        'neutral_percentage': neutral_percentage,
        'average_sentiment': average_sentiment
    }

    return sentiment_analysis_results


def get_sentiment(comment):
    preprocessed_comment = preprocessing(comment)
    sentiments = TextBlob(preprocessed_comment).sentiment.polarity
    return sentiments
