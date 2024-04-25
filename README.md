# practise-image-annotation-service-poc
This is a Proof of Concept (PoC) application of an “Image Annotation Service” where users can perform all the basic actions in order to upload an image and have it annotated.

```mermaid
---
title: Entity Relationship Diagram
---

erDiagram
    User {
        id INT PK
        username VARCHAR
        email VARCHAR
        password_hash VARCHAR
    }

    Image {
        id INT PK
        filename VARCHAR
        user_id INT FK
    }
    
    Comment {
        id INT PK
        body TEXT
        timestamp DATETIME
        user_id INT FK
        image_id INT FK
    }

    Annotation {
        id INT PK
        name VARCHAR
    }

    User ||--o{ Comment : "writes"
    User ||--o{ Image : "uploads"
    Image ||--o{ Comment : "has"
    Image }o--o{ Annotation : "has"
```
