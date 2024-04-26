from uuid import UUID

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer

from app.repos.comment import CommentRepo
from app.repos.image_summary import ImageSummaryRepo


class ImageSummaryService:
    @classmethod
    def initialize(cls):
        nltk.download("punkt")
        nltk.download("vader_lexicon")

    @staticmethod
    def update_image_summary(image_id: UUID):
        # Get all comments for the image
        comments = CommentRepo.get_by_image_id(image_id)
        comment_count = len(comments)

        comment_text = " ".join(comment.body for comment in comments)

        comment_summary = ImageSummaryService.generate_summary(comment_text)
        sentiment_score = ImageSummaryService.calculate_sentiment(comment_text)

        existing_image_summary = ImageSummaryRepo.get_by_image_id(image_id)

        if existing_image_summary:
            ImageSummaryRepo.update(
                summary_id=existing_image_summary.id,
                comment_summary=comment_summary,
                comment_count=comment_count,
                sentiment_score=sentiment_score,
            )

        else:
            ImageSummaryRepo.create(
                image_id, comment_summary, comment_count, sentiment_score
            )

    @staticmethod
    def generate_summary(text: str) -> str:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))

        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentences_count=2)

        return " ".join(str(sentence) for sentence in summary)

    @staticmethod
    def calculate_sentiment(text: str) -> int:
        analyzer = SentimentIntensityAnalyzer()
        sentiment_score = analyzer.polarity_scores(text)["compound"]
        scaled_score = int((sentiment_score + 1) * 50)  # Scale to 0-100 range
        return max(0, min(100, scaled_score))  # Ensure score is within 0-100 range
