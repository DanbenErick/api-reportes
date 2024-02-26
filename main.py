from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import time
from typing import Optional
from reporte import generar_pdf_service
app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hola mundo!"}

nombre_temporal = int(time.time() * 1000)
@app.get('/generar-pdf')
async def generar_pdf(inicio: int, fin: int, area: int, aula: Optional[str] = None, pdf: Optional[str] = nombre_temporal):
    # if not pdf:
    #     pdf = "output"
    try:
        pdf_path = generar_pdf_service(inicio, fin, area, pdf)
        return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))