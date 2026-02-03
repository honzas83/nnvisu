"""nnvisu: Neural Network Training Visualization."""

import importlib.metadata

try:
    __version__ = importlib.metadata.version("nnvisu")
    __metadata__ = importlib.metadata.metadata("nnvisu")
    __author__ = __metadata__.get("Author", "Jan Švec")
except importlib.metadata.PackageNotFoundError:
    # Fallback for local development if not installed
    __version__ = "1.0"
    __author__ = "Jan Švec"
