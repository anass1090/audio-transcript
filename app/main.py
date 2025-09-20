from fastapi import FastAPI
from app.api.routes import router
from app.config import setup_cors

app = FastAPI()

setup_cors(app)
app.include_router(router, prefix="/api")
