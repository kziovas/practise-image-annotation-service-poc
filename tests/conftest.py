# tests/conftest.py

import uuid
from uuid import uuid4

import pytest

from annotations_app import create_app
from app.models.annotation import Annotation
from app.models.comment import Comment
from app.models.image import Image
from app.models.image_summary import ImageSummary
from app.models.user import User
from app.repos.user import UserRepo
from app.services.core_services import db


@pytest.fixture(scope="module")
def app(request):
    """Create and configure a new Flask application for testing."""
    app = create_app()

    # Clear the database before each test
    with app.app_context():
        yield app

    # Delete everything from the database at teardown
    with app.app_context():
        db.session.rollback()  # Ensure no transaction is open
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()


@pytest.fixture(scope="module")
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture(scope="module")
def new_user(app):
    """Create a new user and add it to the test database."""
    with app.app_context():
        user = User(
            username="test_user", email="test@example.com", password_hash="password"
        )
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()


@pytest.fixture
def new_image(app, new_user):
    """Create a new image associated with a new user."""
    with app.app_context():
        image_data = {"user_id": new_user.id, "filename": "test_image.jpg"}
        image = Image(**image_data)
        db.session.add(image)
        db.session.commit()
        yield image
        db.session.delete(image)
        db.session.commit()



@pytest.fixture
def new_image(app, new_user):
    """Create a new image associated with a new user."""
    with app.app_context():
        image_data = {"user_id": new_user.id, "filename": "test_image.jpg"}
        image = Image(**image_data)
        db.session.add(image)
        db.session.commit()
        yield image
        db.session.delete(image)
        db.session.commit()


@pytest.fixture
def new_comment(app, new_user, new_image):
    """Create a new comment associated with a new user and a new image."""
    with app.app_context():
        comment_data = {
            "body": "Test comment",
            "user_id": new_user.id,
            "image_id": new_image.id,
        }
        comment = Comment(**comment_data)
        db.session.add(comment)
        db.session.commit()
        yield comment
        db.session.delete(comment)
        db.session.commit()


@pytest.fixture(scope="module")
def comments(app):
    with app.app_context():
        # Create new users with randomized usernames and emails
        user_data = [
            {
                "username": f"user_{str(uuid.uuid4())[:8]}",
                "email": f"user_{str(uuid.uuid4())[:8]}@example.com",
                "password": "password1",
            },
            {
                "username": f"user_{str(uuid.uuid4())[:8]}",
                "email": f"user_{str(uuid.uuid4())[:8]}@example.com",
                "password": "password2",
            },
            {
                "username": f"user_{str(uuid.uuid4())[:8]}",
                "email": f"user_{str(uuid.uuid4())[:8]}@example.com",
                "password": "password3",
            },
        ]
        users = [UserRepo.create(**data) for data in user_data]

        # Create actual images with real UUIDs
        image_data = [
            {"user_id": users[0].id, "filename": str(uuid.uuid4()) + ".jpg"},
            {"user_id": users[1].id, "filename": str(uuid.uuid4()) + ".jpg"},
            {"user_id": users[2].id, "filename": str(uuid.uuid4()) + ".jpg"},
        ]
        images = [Image(**data) for data in image_data]
        for image in images:
            db.session.add(image)
        db.session.commit()

        # Create comments associated with these users and images
        comment_data = [
            {"body": "Great shot!", "user_id": users[0].id, "image_id": images[0].id},
            {"body": "Nice picture", "user_id": users[1].id, "image_id": images[1].id},
            {"body": "Amazing!", "user_id": users[2].id, "image_id": images[2].id},
        ]
        comments = [Comment(**data) for data in comment_data]
        for comment in comments:
            db.session.add(comment)
        db.session.commit()

        yield comments

        # Clean up after the test
        for comment in comments:
            db.session.delete(comment)
        db.session.commit()

        for image in images:
            db.session.delete(image)
        db.session.commit()

        for user in users:
            UserRepo.delete(user.id)


@pytest.fixture(scope="module")
def new_annotation(app):
    """Create a new annotation."""
    with app.app_context():
        annotation_name = f"Test Annotation"

        # Check if an annotation with the same name already exists
        existing_annotation = Annotation.query.filter_by(name=annotation_name).first()
        if existing_annotation:
            db.session.delete(existing_annotation)
            db.session.commit()

        annotation = Annotation(name=annotation_name)
        db.session.add(annotation)
        db.session.commit()
        yield annotation

        # Clean up after the test
        db.session.delete(annotation)
        db.session.commit()


@pytest.fixture
def new_image_summary(app, new_image):
    """Create a new image summary associated with a new image."""
    with app.app_context():
        summary_data = {
            "image_id": new_image.id,
            "comment_count": 5,
            "comment_summary": "This is a test summary",
            "average_comment_length": 20,
            "users_commented_count": 3,
            "sentiment_score": 75,
        }
        summary = ImageSummary(**summary_data)
        db.session.add(summary)
        db.session.commit()
        yield summary
        db.session.delete(summary)
        db.session.commit()



@pytest.fixture
def image_data():
    return {"user_id": uuid4(), "filename": "test_image.jpg"}
