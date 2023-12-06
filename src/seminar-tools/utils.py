import os


def get_env_variable(name: str):
    var = os.getenv(name)
    if var:
        return var
    else:
        raise ValueError(f"Environment variable {name} not set")
