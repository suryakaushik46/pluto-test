from fastapi import FastAPI
from .routers import pluto
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Declaring the application
app=FastAPI()

# attaching routers to main
app.include_router(pluto.router)

# enabling cors
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/") # sample route
def root():
    """
       _summary_ : start end point
    """
    return{"message":{"tag":"Hello World!!"}}