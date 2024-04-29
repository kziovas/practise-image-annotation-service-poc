class TestImageSummaryModel:
    def test_image_summary_model_creation(self, new_image_summary):
        assert new_image_summary.id is not None
        assert new_image_summary.image_id is not None
        assert new_image_summary.comment_count == 5
        assert new_image_summary.comment_summary == "This is a test summary"
        assert new_image_summary.average_comment_length == 20
        assert new_image_summary.users_commented_count == 3
        assert new_image_summary.sentiment_score == 75
