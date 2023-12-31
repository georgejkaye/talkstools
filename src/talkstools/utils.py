import os
from typing import Optional


def get_env_variable(name: str, default: Optional[str] = None) -> str:
    var = os.getenv(name)
    if var:
        return var
    elif default:
        return default
    else:
        raise ValueError(f"Environment variable {name} not set")


def get_secret(name: str) -> str:
    file = get_env_variable(name)
    if not os.path.isfile(file):
        raise RuntimeError(f"Secret file {file} does not exist")
    with open(file) as f:
        val = f.read().replace("\n", "")
    return val
