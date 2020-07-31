import time

from fastapi import FastAPI

from src import routers
from src.db import engine, Base

app = FastAPI(debug=True, start_date=time.time())

Base.metadata.create_all(bind=engine)
app.include_router(routers.router)
