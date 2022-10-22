"""
Main FastAPI app
"""

from fastapi import FastAPI

from server.routers.user import router as user_router
from server.routers.audio_data import router as audio_router

app = FastAPI(
    title="Concha API 🎧",
    description="Created by: Shiva Reddy",
    version="1.0.1",
    contact={
        "url": "https://github.com/shivajreddy",
    },
)

# Add routers
app.include_router(user_router)
app.include_router(audio_router)


@app.get('/')
def root():
    return {"Name: ": "concha server", "version": "1.0.1", "created by": "Shiva Reddy"}
