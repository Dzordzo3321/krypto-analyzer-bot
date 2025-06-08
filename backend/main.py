from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pytesseract
import numpy as np
import cv2
from PIL import Image
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisResult(BaseModel):
    decision: str
    trend: str
    slope: float
    text: str
    reason: str


def detect_trend(image: np.ndarray):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)
    slopes = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if x2 - x1 != 0:
                slopes.append((y2 - y1) / (x2 - x1))
    avg_slope = float(np.mean(slopes)) if slopes else 0.0
    if avg_slope > 0.05:
        trend = "up"
    elif avg_slope < -0.05:
        trend = "down"
    else:
        trend = "sideways"
    return trend, avg_slope


@app.post("/analyze", response_model=AnalysisResult)
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    image = np.array(Image.open(io.BytesIO(content)))

    trend, slope = detect_trend(image)

    text = pytesseract.image_to_string(Image.open(io.BytesIO(content)))

    if trend == "up":
        decision = "KUP"
        reason = "Trend wzrostowy"
    elif trend == "down":
        decision = "SPRZEDAJ"
        reason = "Trend spadkowy"
    else:
        decision = "TRZYMAJ"
        reason = "Trend boczny lub niepewny"

    if text:
        reason += f". OCR: {text.strip()}"

    return AnalysisResult(decision=decision, trend=trend, slope=slope, text=text, reason=reason)

