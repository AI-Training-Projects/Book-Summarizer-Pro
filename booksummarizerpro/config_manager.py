# Configuration handling
import json
import os

def load_config(filepath):
    if not os.path.exists(filepath):
        default_config = {
            'model': 'bart',
            'chunk_size': 800,
            'chunk_overlap': 200,
            'summary_ratio': 0.1
        }
        save_config(default_config, filepath)
        return default_config
    with open(filepath, 'r') as f:
        return json.load(f)

def save_config(config, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(config, f, indent=4)
