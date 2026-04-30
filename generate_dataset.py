from pathlib import Path
import shutil
from typing import Optional

import kagglehub


DATASET_REF = "mohitkumar282/used-car-dataset"
PRIMARY_FILE = "used_cars_dataset_v2.csv"
SECONDARY_FILE = "used_car_dataset.csv"


def copy_if_present(source_dir: Path, filename: str, target_dir: Path) -> Optional[Path]:
    source_path = source_dir / filename
    if not source_path.exists():
        return None

    target_path = target_dir / filename
    shutil.copy2(source_path, target_path)
    return target_path


def main() -> None:
    repo_dir = Path(__file__).resolve().parent

    print("Downloading latest Kaggle dataset snapshot...")
    dataset_path = Path(kagglehub.dataset_download(DATASET_REF))
    print(f"Dataset cache: {dataset_path}")

    copied = []
    for filename in (PRIMARY_FILE, SECONDARY_FILE):
        target = copy_if_present(dataset_path, filename, repo_dir)
        if target is not None:
            copied.append(target.name)

    if not copied:
        raise FileNotFoundError(
            f"Could not find {PRIMARY_FILE!r} or {SECONDARY_FILE!r} in {dataset_path}"
        )

    print("Available source files copied into the project:")
    for name in copied:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
