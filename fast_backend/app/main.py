from fastapi import FastAPI
from . import product_api
# import product_api

app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/docs"
)

app.include_router(product_api.router)