import os
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from config import settings

MODELS = {}
for key, data in settings.MODEL_CONFIGS.items():
    MODELS[key] = {
        "url": data["url"],
        "filename": data["filename"],
        "path": os.path.join(settings.MODELS_DIR, data["filename"])
    }

def download_file(url, path):
    """Downloads a file from a URL to a local path with a progress indicator."""
    logger.info(f"Downloading {url} to {path}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024 # 1 Kibibyte
    
    with open(path, 'wb') as f:
        for data in response.iter_content(block_size):
            f.write(data)
            
    logger.info(f"Downloaded {path}")

def check_and_download_model(key):
    """Checks if a specific model exists, otherwise downloads it."""
    if not os.path.exists("models"):
        os.makedirs("models")
        
    model_info = MODELS.get(key)
    if not model_info:
        raise ValueError(f"Unknown model key: {key}")

    if not os.path.exists(model_info["path"]):
        logger.info(f"Model {key} not found. Downloading...")
        try:
            download_file(model_info["url"], model_info["path"])
        except Exception as e:
            logger.error(f"Failed to download {key} model: {e}")
            if os.path.exists(model_info["path"]):
                os.remove(model_info["path"])
            raise e
    
    return model_info["path"]
