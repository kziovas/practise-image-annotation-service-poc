from app.repos.comment import CommentRepo


class TestCommentRepo:
    def test_get_all_comments(self, new_comment):
        comments = CommentRepo.get_all()
        assert new_comment in comments

    def test_get_comment_by_id(self, new_comment):
        retrieved_comment = CommentRepo.get_by_id(new_comment.id)
        assert retrieved_comment.id == new_comment.id

    def test_get_comments_by_user_id(self, new_comment):
        comments = CommentRepo.get_by_user_id(new_comment.user_id)
        assert new_comment in comments

    def test_get_comments_by_image_id(self, new_comment):
        comments = CommentRepo.get_by_image_id(new_comment.image_id)
        assert new_comment in comments

    def test_create_comment(self, new_user, new_image):
        body = "Test comment"
        new_comment = CommentRepo.create(
            body=body, user_id=new_user.id, image_id=new_image.id
        )
        assert new_comment is not None
        assert new_comment.body == body

    def test_update_comment(self, new_comment):
        new_body = "Updated comment"
        updated_comment = CommentRepo.update(new_comment.id, body=new_body)
        assert updated_comment is not None
        assert updated_comment.body == new_body

    def test_delete_comment(self, new_comment):
        comment_id = new_comment.id
        assert CommentRepo.delete(comment_id) is True
        assert CommentRepo.get_by_id(comment_id) is None
