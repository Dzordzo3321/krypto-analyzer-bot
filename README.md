# krypto-analyzer-bot

Prosta aplikacja do analizy zrzutów ekranu wykresów kryptowalut.

## Backend

Backend został zbudowany w oparciu o **FastAPI**. Odczytuje tekst z obrazu przy użyciu `pytesseract` oraz wykrywa trend przy użyciu **OpenCV**.

### Uruchomienie backendu

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# system Linux: potrzebny jest pakiet tesseract-ocr
uvicorn main:app --reload --port 8000
```

## Frontend

Frontend to niewielka aplikacja w **React**.

### Uruchomienie frontendu

```bash
cd frontend
npm install
npm start
```

Aplikacja będzie dostępna pod `http://localhost:3000`.

## Sposób działania

1. Wgraj zrzut ekranu wykresu (JPG/PNG).
2. Kliknij **Analizuj**.
3. Po chwili otrzymasz decyzję (KUP/SPRZEDAJ/TRZYMAJ) wraz z uzasadnieniem i odczytanym tekstem z obrazu.
