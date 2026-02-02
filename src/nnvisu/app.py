import asyncio
import importlib.resources
import os
from pathlib import Path

import tornado.web

from nnvisu.handlers import NeuralWebSocket

def make_app() -> tornado.web.Application:
    try:
        # Use importlib.resources to locate the static files within the package
        static_path_traversable = importlib.resources.files("nnvisu").joinpath("static")
        
        # Tornado expects a string or Path object. 
        # Traversable is compatible with Path if on filesystem.
        # We convert to Path/str to be safe.
        static_path = Path(str(static_path_traversable))
        
        if not static_path.exists():
             # Fallback for dev mode without install
             static_path = Path(os.path.dirname(__file__)) / "static"
    except Exception:
        static_path = Path(os.path.dirname(__file__)) / "static"

    return tornado.web.Application([
        (r"/ws", NeuralWebSocket),
        (r"/(.*)", tornado.web.StaticFileHandler, {
            "path": str(static_path), # Convert to string for Tornado compatibility
            "default_filename": "index.html"
        }),
    ])

async def main() -> None:
    app = make_app()
    app.listen(8888)
    print("Server started on http://localhost:8888")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
