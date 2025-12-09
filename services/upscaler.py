import torch
import torchvision.transforms.functional as TF
from spandrel import ModelLoader
from PIL import Image
from utils.model_loader import check_and_download_model
import logging

logger = logging.getLogger(__name__)

from functools import lru_cache
from config import settings

device = "cuda" if torch.cuda.is_available() else "cpu"

@lru_cache(maxsize=settings.MODEL_CACHE_SIZE)
def get_model(mode: str, scale: int):
    """Lazy loads the specific model requested. Cached via LRU."""
    key = f"{mode}_x{scale}"
    
    logger.info(f"Loading model: {key} on {device}...")
    try:
        path = check_and_download_model(key)
        loader = ModelLoader(device=device)
        model = loader.load_from_file(path).model
        model.eval()
        return model
    except ValueError:
        raise ValueError(f"Unsupported configuration: Mode '{mode}', Scale '{scale}x'")

def upscale_image(image: Image.Image, mode: str, scale: int) -> Image.Image:
    model = get_model(mode, scale)
    
    # Convert PIL to Tensor (C, H, W)
    img_t = TF.to_tensor(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        output_t = model(img_t)
    
    # Postprocess
    output_t = output_t.squeeze(0).clamp(0, 1)
    output_img = TF.to_pil_image(output_t.cpu())
    
    return output_img
