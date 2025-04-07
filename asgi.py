"""ASGI Entry Point

This file provides the ASGI application instance ('app') for ASGI servers
like Uvicorn, Daphne, or Hypercorn.

It also allows running the application directly using Uvicorn for local
development.
"""

# --- Development Server Execution ---
# The code within this 'if' block runs ONLY when this script is executed
# directly (e.g., `python asgi.py`). It starts Uvicorn's development server.
# This is NOT typically used in production.
if __name__ == '__main__':
    import uvicorn

    # `reload=True` is useful for development as it automatically restarts
    # the server when code changes are detected.
    # `host="0.0.0.0"` makes the server accessible from other devices on the network.
    # Use `host="127.0.0.1"` (default) to only allow connections from the local machine.
    uvicorn.run(
        'service.main:app',  # Points Uvicorn to the 'app'
        host="127.0.0.1",
        port=8000,
        reload=True  # Enable auto-reload for development
    )
