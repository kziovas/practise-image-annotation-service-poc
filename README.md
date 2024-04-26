# practise-image-annotation-service-poc
This is a Proof of Concept (PoC) application of an “Image Annotation Service” where users can perform all the basic actions in order to upload an image and have it annotated.

```mermaid
---
title: Entity Relationship Diagram
---

erDiagram
    User {
        id UUID PK
        username VARCHAR
        email VARCHAR
        password_hash VARCHAR
        created_at DATETIME
        updated_at DATETIME
        deleted_at DATETIME
    }

    Image {
        id UUID PK
        filename VARCHAR
        user_id UUID FK
        annotation_status ENUM
        created_at DATETIME
        updated_at DATETIME
        deleted_at DATETIME
    }

    Comment {
        id UUID PK
        body TEXT
        user_id UUID FK
        image_id UUID FK
        created_at DATETIME
        updated_at DATETIME
        deleted_at DATETIME
    }

    Annotation {
        id UUID PK
        name VARCHAR
        created_at DATETIME
        updated_at DATETIME
        deleted_at DATETIME
    }

    ImageSummary {
        id UUID PK
        image_id UUID FK
        comment_summary TEXT
        comment_sentiments_score INTEGER
        created_at DATETIME
        updated_at DATETIME
        deleted_at DATETIME
    }

    User ||--o{ Comment : "writes"
    User ||--o{ Image : "uploads"
    Image ||--o{ Comment : "has"
    Image }o--o{ Annotation : "has"
    Image ||--|| ImageSummary : "has"

```
