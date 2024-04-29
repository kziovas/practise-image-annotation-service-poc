from app.repos.image_summary import ImageSummaryRepo


class TestImageSummaryRepo:
    def test_get_all_image_summaries(self, new_image_summary):
        summaries = ImageSummaryRepo.get_all()
        assert new_image_summary in summaries

    def test_get_image_summary_by_id(self, new_image_summary):
        retrieved_summary = ImageSummaryRepo.get_by_id(new_image_summary.id)
        assert retrieved_summary.id == new_image_summary.id

    def test_get_image_summary_by_image_id(self, new_image_summary):
        retrieved_summary = ImageSummaryRepo.get_by_image_id(new_image_summary.image_id)
        assert retrieved_summary.id == new_image_summary.id

    def test_create_image_summary(self, new_image):
        summary_data = {
            "image_id": new_image.id,
            "comment_count": 8,
            "comment_summary": "New summary",
            "average_comment_length": 15,
            "users_commented_count": 4,
            "sentiment_score": 80,
        }
        new_summary = ImageSummaryRepo.create(**summary_data)
        assert new_summary is not None
        assert new_summary.comment_count == 8
        assert new_summary.comment_summary == "New summary"
        assert new_summary.average_comment_length == 15
        assert new_summary.users_commented_count == 4
        assert new_summary.sentiment_score == 80

    def test_update_image_summary(self, new_image_summary):
        new_comment_count = 15
        new_summary = "Updated summary"
        updated_image_summary = ImageSummaryRepo.update(
            new_image_summary.id,
            comment_count=new_comment_count,
            comment_summary=new_summary,
        )
        assert updated_image_summary.comment_count == new_comment_count
        assert updated_image_summary.comment_summary == new_summary

    def test_delete_image_summary(self, new_image_summary):
        summary_id = new_image_summary.id
        assert ImageSummaryRepo.delete(summary_id) is True
        assert ImageSummaryRepo.get_by_id(summary_id) is None
