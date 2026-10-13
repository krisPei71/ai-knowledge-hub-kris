from fastapi import FastAPI
from app import models
from app.database import Base,engine
from app.router import auth,ticket

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(ticket.router)

@app.get('/health')
def health():
    return {"status":"ok"}