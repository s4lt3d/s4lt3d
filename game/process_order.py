#!/usr/bin/env python3
"""Process an incoming order: update state.json, then call the SVG generator."""
import json, os, sys, re

script_dir = os.path.dirname(os.path.abspath(__file__))
state_path = os.path.join(script_dir, 'state.json')

# Load current state
if os.path.exists(state_path):
    with open(state_path) as f:
        data = json.load(f)
else:
    data = {'state': 'idle', 'last_order': None, 'order_count': 0}

# Parse order type from first argument (issue title)
title = sys.argv[1].lower() if len(sys.argv) > 1 else ''
if 'coffee' in title:
    data['state'] = 'serving_coffee'
    data['last_order'] = 'coffee'
elif 'pastry' in title:
    data['state'] = 'serving_pastry'
    data['last_order'] = 'pastry'
else:
    print(f"Unknown order: {title!r} — ignoring")
    sys.exit(0)

data['order_count'] = data.get('order_count', 0) + 1

with open(state_path, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Order: {data['state']}  (total: {data['order_count']})")

# Update cache-busting version in README
readme_path = os.path.join(script_dir, '..', 'README.md')
if os.path.exists(readme_path):
    with open(readme_path) as f:
        content = f.read()
    content = re.sub(
        r'coffee-shop\.svg\?v=\d+',
        f"coffee-shop.svg?v={data['order_count']}",
        content
    )
    with open(readme_path, 'w') as f:
        f.write(content)
    print(f"README cache-buster updated to v={data['order_count']}")
