import asyncio
import os

import tornado.web

from handlers import NeuralWebSocket
from logic.model import TrainingState

# Global state (simple in-memory for this demo)
state = TrainingState(points=[])

def make_app() -> tornado.web.Application:
    # Get the frontend path relative to this file
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/src"))

    return tornado.web.Application([
        (r"/ws", NeuralWebSocket, {"state": state}),
        (r"/(.*)", tornado.web.StaticFileHandler, {
            "path": frontend_path,
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
