from pathlib import Path
import ast
import os


BASE_DIR = Path(__file__).resolve().parent.parent


if not Path.exists(BASE_DIR / '.env'):
    raise Exception(
        "Hi it's me GUSS, I did not find .env file in the root directory, please add .env file with your credentials!")
else:
    from dotenv import load_dotenv

    load_dotenv(BASE_DIR / '.env')

DATA_DIR = BASE_DIR / "data"
DATA_INPUT =  DATA_DIR/"input"
DATA_OUTPUT = DATA_DIR / "output"
CSV_OUTPUT = DATA_OUTPUT/ "csv"
SHP_OUTPUT = DATA_OUTPUT/'shp'
GPK_OUTPUT = DATA_OUTPUT/'gpkg'


for dir in [DATA_DIR, DATA_INPUT, DATA_OUTPUT, CSV_OUTPUT, SHP_OUTPUT, GPK_OUTPUT]:
    if not Path.exists(dir):
        Path.mkdir(dir)


