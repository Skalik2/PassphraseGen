import json
import os
from config import STORAGE_FILE

def load_passphrases():
    if not os.path.exists(STORAGE_FILE):
        return []
    try:
        with open(STORAGE_FILE, 'r') as f:
            data = json.load(f)
            return data
    except (json.JSONDecodeError, IOError):
        return []

def save_passphrases(data):
    try:
        with open(STORAGE_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except IOError:
        return False

def add_passphrase_entry(name, url, passphrase_to_store):
    entries = load_passphrases()
    for entry in entries:
        if entry.get("name") == name:
            return False
    entries.append({"name": name, "url": url, "passphrase": passphrase_to_store})
    return save_passphrases(entries)

def delete_passphrase_entry(name_to_delete):
    entries = load_passphrases()
    updated_entries = [entry for entry in entries if entry.get("name") != name_to_delete]
    
    if len(updated_entries) < len(entries):
        return save_passphrases(updated_entries)
    return False