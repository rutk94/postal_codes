import os
from dotenv import load_dotenv
from pathlib import Path


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
