from dataclasses import dataclass
from typing import List

@dataclass
class AnnotationResponse:
    id: int
    name: str
    images: List[int]
