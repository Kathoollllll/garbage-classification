import os
import io
import numpy as np
import tensorflow as tf
from PIL import Image
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Initialize FastAPI
app = FastAPI()

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'garbage_model.keras')
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif'}

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load Model
MODEL = None
try:
    if os.path.exists(MODEL_PATH):
        MODEL = tf.keras.models.load_model(MODEL_PATH)
        print("✅ Garbage Classification Model loaded successfully.")
    else:
        print(f"⚠️ Model file not found at {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error loading model: {e}")

def predict_image(image: Image.Image):
    if MODEL is None:
        return None
    try:
        # Match your trained input size (150x150)
        img = image.convert('RGB').resize((150, 150))
        arr = np.asarray(img) / 255.0
        arr = np.expand_dims(arr, axis=0)
        
        preds = MODEL.predict(arr)
        classes = ['Battery', 'Cardboard', 'Clothes', 'Glass', 'Metal', 'Paper', 'Plastic']
        
        idx = int(np.argmax(preds[0]))
        confidence = float(np.max(preds[0]))
        
        return {'label': classes[idx], 'confidence': confidence}
    except Exception as e:
        print(f"Prediction Error: {e}")
        return None

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"active_page": "home"}
    )

@app.get("/features", response_class=HTMLResponse)
async def features(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="features.html",
        context={"active_page": "features", "model_loaded": MODEL is not None}
    )

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={"active_page": "about"}
    )

@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    # 1. Validate File Extension
    filename = image.filename.lower()
    if not any(filename.endswith(ext) for ext in ALLOWED_EXT):
        return JSONResponse(
            status_code=400, 
            content={"error": f"Unsupported file type. Allowed: {ALLOWED_EXT}"}
        )

    try:
        # 2. Read image stream
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))
        
        # 3. Run Prediction
        result = predict_image(img)
        
        if result is None:
            return JSONResponse(status_code=500, content={"error": "Prediction failed"})
            
        return result
        
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": "Invalid image file"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)