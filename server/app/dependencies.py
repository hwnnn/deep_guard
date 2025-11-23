from .core_config import get_settings
from .services.face_swap.dummy_model import DummyFaceSwapModel

# In a real scenario, swap this with an actual deepfake face swap model loader.
face_swap_model = DummyFaceSwapModel()

def get_face_swap_model():
    return face_swap_model

def get_app_settings():
    return get_settings()