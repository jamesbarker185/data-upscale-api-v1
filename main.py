from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from services.upscaler import upscale_image
from PIL import Image
import io
import logging
import asyncio
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

@app.post("/upscale")
async def upscale(file: UploadFile = File(...), mode: str = Form(...), scale: int = Form(...)):
    if mode not in ["fidelity", "aesthetic"]:
        raise HTTPException(status_code=400, detail="Invalid mode. use 'fidelity' or 'aesthetic'")
    
    if scale not in [2, 4]:
        raise HTTPException(status_code=400, detail="Invalid scale. use 2 or 4")
    
    try:
        logger.info(f"Processing image: mode={mode}, scale={scale}x")
        # Read image efficiently from spooled file
        image = Image.open(file.file).convert("RGB")
        logger.info(f"Image loaded: {image.size}")

        if image.width > settings.MAX_IMAGE_WIDTH or image.height > settings.MAX_IMAGE_HEIGHT:
            raise HTTPException(status_code=400, detail=f"Image too large. Max size is {settings.MAX_IMAGE_WIDTH}x{settings.MAX_IMAGE_HEIGHT}")
        
        # Upscale (run in threadpool to avoid blocking event loop)
        result_image = await asyncio.to_thread(upscale_image, image, mode, scale)
        logger.info(f"Upscale complete. New size: {result_image.size}")
        
        # Return as PNG
        img_byte_arr = io.BytesIO()
        result_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)
        
        return StreamingResponse(img_byte_arr, media_type="image/png")
    
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
