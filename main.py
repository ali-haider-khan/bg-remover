from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
import io

app = FastAPI(title="Production Background Removal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Render has 1GB disk space, so we can use the high-quality model safely!
# session = new_session("u2net")
session = new_session("u2netp")

@app.get("/")
def home():
    # Redirect base URL to interactive documentation automatically
    return RedirectResponse(url="/docs")

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    image_bytes = await file.read()
    output_bytes = remove(image_bytes, session=session)
    return StreamingResponse(io.BytesIO(output_bytes), media_type="image/png")
