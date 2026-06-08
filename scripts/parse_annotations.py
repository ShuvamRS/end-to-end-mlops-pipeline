import json
import shutil
from pathlib import Path

EXTRA_DATA_FOLDER_PATH = Path("extra-data/extra_data")
NEW_DATA_FOLDER_PATH = Path("data/raw")

with open("extra-data/annotations.json") as f:
    annotations = json.load(f)

for annotation in annotations:
    filename = "".join(annotation["image"].split("-")[1:])
    choice = annotation["choice"]

    source_path = EXTRA_DATA_FOLDER_PATH / filename
    dest_path = NEW_DATA_FOLDER_PATH / choice / filename

    print(f"Copying {source_path} -> {dest_path}")
    shutil.copy(source_path, dest_path)
