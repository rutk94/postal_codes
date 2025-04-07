import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from src.settings_func import get_integer_or_none


load_dotenv(override=True)

MAIN_PATH: Path = Path(__file__).parent.parent
OUTPUT_DIR: Path = MAIN_PATH / 'output'
POSTAL_CODES_PATH: Path = Path(
    os.getenv(
        'POSTAL_CODES_PATH', default=MAIN_PATH / 'resources' / 'lista-kodow-2018.xlsx'
    )
)
MAP_SHAPE_PATH: Path = Path(
    os.getenv('MAP_SHAPE_PATH', default=MAIN_PATH / 'resources' / 'map-shape.geojson')
)
SEED: Optional[int] = get_integer_or_none('SEED')
MAX_TOTAL_DISTANCE: Optional[int] = get_integer_or_none(
    'MAX_TOTAL_DISTANCE', default=10_000_000
)
SOLUTION_LIMIT: Optional[int] = get_integer_or_none(
    'SOLUTION_LIMIT', default=10_000_000
)
TIME_LIMIT: Optional[int] = get_integer_or_none('TIME_LIMIT', default=60)
