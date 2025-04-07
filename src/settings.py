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