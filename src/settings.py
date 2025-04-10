import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from src.settings_func import get_integer_or_none, get_integer_or_die, get_float_or_die

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
MAX_TOTAL_DISTANCE: int = get_integer_or_die('MAX_TOTAL_DISTANCE', default=10_000_000)
SOLUTION_LIMIT: int = get_integer_or_die('SOLUTION_LIMIT', default=10_000_000)
TIME_LIMIT: int = get_integer_or_die('TIME_LIMIT', default=60)
CAPACITY_FACTOR: float = get_float_or_die('CAPACITY_FACTOR', default=1.1)
