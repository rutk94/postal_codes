import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


load_dotenv(override=True)

MAIN_PATH: Path = Path(__file__).parent.parent
POSTAL_CODES_PATH: Path = Path(
    os.getenv(
        'POSTAL_CODES_PATH', default=MAIN_PATH / 'resources' / 'lista-kodow-2018.xlsx'
    )
)
MAP_SHAPE_PATH: Path = Path(
    os.getenv(
        'MAP_SHAPE_PATH', default=MAIN_PATH / 'resources' / 'map-shape.geojson'
    )
)

SEED_STR: str = str(os.getenv('SEED'))
SEED: Optional[int] = int(SEED_STR) if SEED_STR.isdigit() else None

MAX_TOTAL_DISTANCE_STR: str = str(os.getenv('MAX_TOTAL_DISTANCE', default=10_000_000)).replace('_', '')
MAX_TOTAL_DISTANCE: int = int(MAX_TOTAL_DISTANCE_STR) if MAX_TOTAL_DISTANCE_STR.isdigit() else None

SOLUTION_LIMIT_STR: str = str(os.getenv('SOLUTION_LIMIT', default=10_000_000)).replace('_', '')
SOLUTION_LIMIT: int = int(SOLUTION_LIMIT_STR) if SOLUTION_LIMIT_STR.isdigit() else None

TIME_LIMIT_STR: str = str(os.getenv('TIME_LIMIT', default=60)).replace('_', '')
TIME_LIMIT: int = int(TIME_LIMIT_STR) if TIME_LIMIT_STR.isdigit() else None