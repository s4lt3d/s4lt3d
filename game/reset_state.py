#!/usr/bin/env python3
"""Reset game state back to idle."""
import json, os

script_dir = os.path.dirname(os.path.abspath(__file__))
state_path = os.path.join(script_dir, 'state.json')

with open(state_path) as f:
    data = json.load(f)

data['state'] = 'idle'

with open(state_path, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Reset to idle  (total orders: {data['order_count']})")
