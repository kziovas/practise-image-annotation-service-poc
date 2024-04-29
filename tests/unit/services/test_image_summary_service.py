from app.models.image_summary import ImageSummary
from app.repos.image_summary import ImageSummaryRepo
from app.services.image_summary_service import ImageSummaryService


class TestImageSummaryService:
    def test_generate_summary(self):
        text = "This is a test comment. It contains some random text."
        summary = ImageSummaryService.generate_summary(text)
        assert isinstance(summary, str)

    def test_calculate_sentiment(self):
        text = "This is a test comment. It contains some random text."
        sentiment_score = ImageSummaryService.calculate_sentiment(text)
        assert isinstance(sentiment_score, int)
        assert 0 <= sentiment_score <= 100

    def test_update_image_summary(self, comments):
        image_id = comments[0].image_id

        ImageSummaryService.update_image_summary(image_id)

        image_summary = ImageSummaryRepo.get_by_image_id(image_id)
        assert image_summary is not None
        assert isinstance(image_summary, ImageSummary)

        ImageSummaryRepo.delete(image_summary.id)
