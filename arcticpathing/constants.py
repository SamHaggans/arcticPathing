from pathlib import Path

PACKAGE_DIR = Path(__file__).parent
PROJECT_DIR = PACKAGE_DIR.parent
DATA_DIR = PROJECT_DIR / 'ice_data'

DATASET_PATH = DATA_DIR / 'RDEFT4_20200229.nc'
LAND_MASK_PATH = DATA_DIR / 'gsfc_25n.msk'

GRID_SIZE = 25  # km
DATA_PRECISION = 3
