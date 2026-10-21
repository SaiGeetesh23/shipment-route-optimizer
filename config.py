"""Central application configuration."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SHIPMENTS_PATH = DATA_DIR / "shipments.csv"
ROUTES_PATH = DATA_DIR / "routes.csv"

PAGE_TITLE = "Aiqon | Route Intelligence"
PAGE_ICON = ""
DEFAULT_SHIPMENT_ID = "SH003"

FEASIBLE_COLOR = "#8A5A3B"
REJECTED_COLOR = "#B4533C"
INK = "#49372B"
MUTED = "#78685B"
LINE = "#E7DCCB"
PANEL = "#FFFCF6"
BACKGROUND = "#F5EFE4"
ACCENT = "#8A5A3B"
