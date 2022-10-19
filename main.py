"""
Starting point of the application
"""

from fastapi import FastAPI

# Routers
from server.routers.user import router as user_router
from server.routers.audioDataFile import router as audio_router

app = FastAPI(
    title="Concha API 🎧",
    description="Created by: Shiva Reddy",
    version="1.0.1",
    contact={
        "url": "https://github.com/shivajreddy",
    },
)

# include the routers

app.include_router(user_router)
app.include_router(audio_router)

