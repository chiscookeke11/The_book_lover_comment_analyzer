import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


#  first we clean the text
def clean_text(text: str):
    text = text.lower()
    text = re.sub(r"([^\w\s])", "", text)
    return text



# then we analyze the text
def analyze_sentiment(text: str):
    clean = clean_text(text)
    score = analyzer.polarity_scores(clean)["compound"]

    if score > 0.1:
        label = "positive"

    elif score < -0.1:
        label = "negative"

    else:
        label = "neutral"


    return {
        "label": label,
        "score": score
    }
