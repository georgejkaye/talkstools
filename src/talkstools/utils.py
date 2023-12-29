import os
from typing import Optional


def get_env_variable(name: str, default: Optional[str] = None):
    var = os.getenv(name)
    if var:
        return var
    elif default:
        return default
    else:
        raise ValueError(f"Environment variable {name} not set")
