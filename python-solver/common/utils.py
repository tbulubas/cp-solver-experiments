from typing import Any
from pathlib import Path
import json

from importlib_resources import files
import yaml


def load_config(file_name='config.yaml'):
    file_path = get_resource_file_for_module("common", file_name)
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def get_resource_file_for_module(module: str, name: str) -> Any:
    if files(module).joinpath(name).is_file():
        return files(module).joinpath(name)
    return None


def load_json_from_subdir(subdir: str, filename: str):
    import os
    from pathlib import Path

    # Step up to project root (assumes script is in project_root/any/subdir/)
    base_path = Path(__file__).resolve().parent
    while not (base_path / ".git").exists() and base_path.name != "python-solver":
        base_path = base_path.parent

    full_path = base_path / subdir / filename

    if not full_path.exists():
        raise FileNotFoundError(f"File not found: {full_path}")

    with full_path.open("r", encoding="utf-8") as f:
        return json.load(f)
