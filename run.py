"""
Starting point of the application
"""

import uvicorn
from server import app
from server.config import settings

if __name__ == "__main__":
    uvicorn.run(app, host=settings.server_address, port=settings.server_port, log_level="info")
