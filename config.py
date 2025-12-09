import os

class Settings:
    # Service Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8080))
    ENV = os.getenv("ENV", "development")

    # Image Processing Limits
    MAX_IMAGE_WIDTH = 2048
    MAX_IMAGE_HEIGHT = 2048
    MAX_FILE_SIZE_MB = 10

    # Model Configuration
    MODEL_CACHE_SIZE = int(os.getenv("MODEL_CACHE_SIZE", 2))
    
    # Model URLs and Paths
    MODELS_DIR = "models"
    MODEL_CONFIGS = {
        "fidelity_x4": {
            "url": "https://github.com/JingyunLiang/SwinIR/releases/download/v0.0/003_realSR_BSRGAN_DFOWMFC_s64w8_SwinIR-L_x4_GAN.pth",
            "filename": "SwinIR-L_x4_GAN.pth",
        },
        "aesthetic_x4": {
            "url": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",
            "filename": "RealESRGAN_x4plus.pth",
        },
        "fidelity_x2": {
            "url": "https://github.com/JingyunLiang/SwinIR/releases/download/v0.0/003_realSR_BSRGAN_DFO_s64w8_SwinIR-M_x2_GAN.pth",
            "filename": "SwinIR-M_x2_GAN.pth",
        },
        "aesthetic_x2": {
            "url": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth",
            "filename": "RealESRGAN_x2plus.pth",
        }
    }

settings = Settings()
