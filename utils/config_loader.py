import yaml
import os

DEFAULT_CONFIG = {
    "max_threads": 100,
    "default_timeout": 0.5
}

def load_config():
    if not os.path.exists("config.yaml"):
        return DEFAULT_CONFIG

    with open("config.yaml", "r") as f:
        user_config = yaml.safe_load(f)

    if not user_config:
        return DEFAULT_CONFIG

    return {**DEFAULT_CONFIG, **user_config}