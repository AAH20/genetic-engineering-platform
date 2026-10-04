"""Pytest configuration: ensure project root is importable in all environments."""
import sys
from pathlib import Path

ROOT = str(Path(__file__).parent)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
