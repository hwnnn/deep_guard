from abc import ABC, abstractmethod
from typing import BinaryIO

class FaceSwapModel(ABC):
    """Abstract interface for a face swap model.

    Contract:
    - initialize heavy models/resources in __init__.
    - swap(source_bytes, target_bytes) -> result image bytes (PNG/JPEG)
    """

    @abstractmethod
    def swap(self, source: bytes, target: bytes) -> bytes:
        """Perform face swap using source face onto target image.
        Returns raw bytes of the resulting image file.
        """
        raise NotImplementedError
