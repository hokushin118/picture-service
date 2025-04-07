"""ASGI Entry Point - for development servers

This file is used to expose the FastAPI application instance ('app')
to ASGI servers like Gunicorn or Uvicorn.
"""
from service.main import app  # Import FastAPI application

# This block is for development purposes only.
# It runs the FastAPI application directly using Uvicorn.
# It is executed when this file is run directly (e.g., 'python wsgi.py').
if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000)
# For WSGI servers: (This is what the WSGI server will use)
# It points to the FastAPI application instance.
application = app
