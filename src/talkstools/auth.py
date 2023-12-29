from dataclasses import dataclass
import json
import os
from pathlib import Path

from talkstools.utils import get_env_variable


def read_credentials() -> dict:
    file = get_env_variable("TALKSTOOLS_CREDENTIALS", default="credentials.json")
    if not os.path.exists(file):
        raise FileNotFoundError("Could not find credentials file")
    with open(file) as f:
        data = json.load(f)
    return data
