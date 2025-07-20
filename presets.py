import os
import json
from config import BASE

# Presets stored in <project_root>/presets.json
PRESETS_FILE = os.path.join(BASE, "presets.json")

def _load_presets():
    """Internal: load all presets from file, return dict."""
    if os.path.exists(PRESETS_FILE):
        try:
            with open(PRESETS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def _save_presets(presets):
    """Internal: save the full presets dict to file."""
    os.makedirs(os.path.dirname(PRESETS_FILE), exist_ok=True)
    with open(PRESETS_FILE, "w") as f:
        json.dump(presets, f, indent=4)

def save_preset(name, settings):
    """
    Save or update a preset.
    :param name: str, preset identifier
    :param settings: dict, watermark settings to store
    """
    presets = _load_presets()
    presets[name] = settings
    _save_presets(presets)

def load_preset(name):
    """
    Load a single preset by name.
    :return: dict or None if not found
    """
    return _load_presets().get(name)

def list_presets():
    """
    List all saved preset names.
    :return: list of str
    """
    return list(_load_presets().keys())

def delete_preset(name):
    """
    Remove a preset by name.
    :param name: str, preset to delete
    """
    presets = _load_presets()
    if name in presets:
        del presets[name]
        _save_presets(presets)
