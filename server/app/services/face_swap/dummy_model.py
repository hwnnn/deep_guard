"""A lightweight dummy face swap implementation.
This does NOT perform real deepfake swapping. It simply composites two images
or returns the target image if compositing fails. Replace with a real model later.
"""
from io import BytesIO
from PIL import Image
from .base import FaceSwapModel

class DummyFaceSwapModel(FaceSwapModel):
    def __init__(self):
        # Placeholder for loading a heavy ML model.
        self.name = "dummy"

    def swap(self, source: bytes, target: bytes) -> bytes:
        try:
            src_img = Image.open(BytesIO(source)).convert("RGBA")
            tgt_img = Image.open(BytesIO(target)).convert("RGBA")
            # Resize source to 30% of target width and simple paste at top-left.
            new_w = max(1, tgt_img.width // 3)
            ratio = new_w / src_img.width
            resized = src_img.resize((new_w, int(src_img.height * ratio)))
            composite = tgt_img.copy()
            composite.paste(resized, (10, 10), resized)
            out_buffer = BytesIO()
            composite.convert("RGB").save(out_buffer, format="JPEG")
            return out_buffer.getvalue()
        except Exception:
            # Fallback: just return target
            return target
