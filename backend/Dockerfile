# Basis-Image
FROM python:3.13-alpine

# Arbeitsverzeichnis setzen
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Code kopieren
COPY . .

# Expose Port 8000 für FastAPI
EXPOSE 8000

# Startkommando für die App
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
