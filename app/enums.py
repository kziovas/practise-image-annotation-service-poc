from enum import Enum


class AnnotationStatus(Enum):
    Queued = "Queued"
    Processing = "Processing"
    Success = "Success"
    Fail = "Fail"
