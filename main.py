from fastapi import FastAPI
from app.routers import router as seo

app = FastAPI()
app.include_router(seo)