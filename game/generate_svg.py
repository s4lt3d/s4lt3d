#!/usr/bin/env python3
"""Pixel art coffee shop SVG generator for GitHub profile README."""
import json, os

U = 8          # px per grid unit
GW, GH = 75, 34  # grid dimensions → 600 × 272 px

C = {
    'wall':         '#F2D9A0',
    'wall_stripe':  '#E8CE8C',
    'floor':        '#8B6533',
    'floor_dark':   '#7A5525',
    'counter_top':  '#2C1606',
    'counter_face': '#4A2810',
    'counter_shine':'#5E3218',
    'win_frame':    '#5C3A1E',
    'win_sky':      '#87CEEB',
    'win_cloud':    '#FFFFFF',
    'board':        '#1A3020',
    'board_trim':   '#2E5038',
    'chalk':        '#EEEEEE',
    'chalk_yellow': '#F5E642',
    'chalk_dim':    '#AAAAAA',
    'mach_body':    '#ABABAB',
    'mach_dark':    '#808080',
    'mach_shine':   '#D0D0D0',
    'mach_black':   '#111111',
    'mach_green':   '#00CC44',
    'mach_red':     '#CC2200',
    'mach_steam':   '#CCCCCC',
    'case_frame':   '#C8B09A',
    'case_glass':   '#D8EEF8',
    'case_shelf':   '#7A5525',
    'croissant':    '#E8C070',
    'croissant_d':  '#C8980A',
    'muffin':       '#7B3A10',
    'muffin_top':   '#A05020',
    'cookie':       '#D4A860',
    'bar_hair':     '#2A1005',
    'bar_skin':     '#F5C99A',
    'bar_shirt':    '#FFFFFF',
    'bar_apron':    '#2255BB',
    'cust_hair':    '#1A1A1A',
    'cust_skin':    '#F5C99A',
    'cust_shirt':   '#BB3333',
    'cust_pants':   '#334466',
    'cup_body':     '#F0EDE0',
    'cup_coffee':   '#5A2D0C',
    'cup_sleeve':   '#C04422',
    'box_body':     '#F4E3C1',
    'box_lid':      '#E8D0A8',
    'box_ribbon':   '#CC4488',
}


def px(v): return v * U


def r(x, y, w, h, c, eid="", cls=""):
    attrs = f' id="{eid}"' if eid else ''
    attrs += f' class="{cls}"' if cls else ''
    return (f'<rect x="{px(x)}" y="{px(y)}" '
            f'width="{px(w)}" height="{px(h)}" fill="{c}"{attrs}/>')


def get_styles(state):
    steam_anim = """
    @keyframes steam {
      0%   { opacity: 0; transform: translateY(0); }
      35%  { opacity: 0.7; }
      100% { opacity: 0; transform: translateY(-28px); }
    }
    .s1 { animation: steam 2.4s ease-out infinite; }
    .s2 { animation: steam 2.4s ease-out 0.8s infinite; }
    .s3 { animation: steam 2.4s ease-out 1.6s infinite; }"""

    if state == 'idle':
        return f"""<style>
    @keyframes walk-in {{
      0%   {{ transform: translateX(184px); }}
      75%  {{ transform: translateX(0); }}
      100% {{ transform: translateX(0); }}
    }}
    @keyframes bob {{
      0%, 100% {{ transform: translateY(0); }}
      50%       {{ transform: translateY(-4px); }}
    }}
    {steam_anim}
    #cx {{ animation: walk-in 1.8s cubic-bezier(.2,.8,.4,1) forwards; }}
    #cy {{ animation: bob 1.1s ease-in-out 1.8s infinite; }}
  </style>"""

    elif state == 'serving_coffee':
        return f"""<style>
    @keyframes bob {{
      0%, 100% {{ transform: translateY(0); }}
      50%       {{ transform: translateY(-3px); }}
    }}
    @keyframes reach {{
      0%   {{ transform: translateX(0); }}
      60%  {{ transform: translateX(-10px); }}
      100% {{ transform: translateX(-10px); }}
    }}
    @keyframes cup-rise {{
      0%   {{ transform: translateY(16px); opacity: 0; }}
      55%  {{ transform: translateY(0); opacity: 1; }}
      100% {{ transform: translateY(0); opacity: 1; }}
    }}
    {steam_anim}
    #cx {{ animation: reach 1.1s ease-out 0.4s forwards; }}
    #cy {{ animation: bob 1.1s ease-in-out infinite; }}
    #cup {{ animation: cup-rise 0.9s ease-out forwards; }}
  </style>"""

    elif state == 'serving_pastry':
        return f"""<style>
    @keyframes bob {{
      0%, 100% {{ transform: translateY(0); }}
      50%       {{ transform: translateY(-3px); }}
    }}
    @keyframes reach {{
      0%   {{ transform: translateX(0); }}
      60%  {{ transform: translateX(-10px); }}
      100% {{ transform: translateX(-10px); }}
    }}
    @keyframes box-slide {{
      0%   {{ transform: translateX(-40px); opacity: 0; }}
      60%  {{ transform: translateX(0); opacity: 1; }}
      100% {{ transform: translateX(0); opacity: 1; }}
    }}
    {steam_anim}
    #cx {{ animation: reach 1.1s ease-out 0.4s forwards; }}
    #cy {{ animation: bob 1.1s ease-in-out infinite; }}
    #box {{ animation: box-slide 0.9s ease-out 0.2s forwards; }}
  </style>"""

    return '<style></style>'


def build_scene():
    out = []
    # Wall
    out.append(r(0, 0, GW, 21, C['wall']))
    for col in range(0, GW, 12):
        out.append(r(col, 0, 1, 21, C['wall_stripe']))
    # Floor
    out.append(r(0, 21, GW, GH - 21, C['floor']))
    for fy in range(21, GH, 3):
        out.append(r(0, fy, GW, 1, C['floor_dark']))

    # Window (left wall)
    out.append(r(3, 1, 22, 17, C['win_frame']))   # outer frame
    out.append(r(4, 2, 20, 15, C['win_sky']))      # sky
    out.append(r(6, 3, 5, 2, C['win_cloud']))      # cloud 1
    out.append(r(13, 4, 6, 2, C['win_cloud']))     # cloud 2
    out.append(r(10, 5, 3, 1, C['win_cloud']))     # cloud wisp
    out.append(r(14, 2, 1, 15, C['win_frame']))    # vertical divider
    out.append(r(4, 10, 20, 1, C['win_frame']))    # horizontal divider
    out.append(r(2, 18, 24, 1, C['win_frame']))    # sill

    # Menu board (right wall)
    out.append(r(50, 1, 24, 1, C['board_trim']))
    out.append(r(50, 1, 24, 14, C['board']))
    out.append(r(50, 14, 24, 1, C['board_trim']))
    out.append(r(50, 1, 1, 14, C['board_trim']))
    out.append(r(73, 1, 1, 14, C['board_trim']))
    out.append(f'<text x="{px(62)}" y="{px(5)}" font-family="monospace" '
               f'font-size="12" font-weight="bold" fill="{C["chalk_yellow"]}" '
               f'text-anchor="middle" letter-spacing="2">MENU</text>')
    out.append(f'<line x1="{px(51)}" y1="{px(6)}" x2="{px(73)}" y2="{px(6)}" '
               f'stroke="{C["chalk_dim"]}" stroke-width="1"/>')
    out.append(f'<text x="{px(53)}" y="{px(9)}" font-family="monospace" '
               f'font-size="10" fill="{C["chalk"]}">&#9749; Coffee</text>')
    out.append(f'<text x="{px(53)}" y="{px(12)}" font-family="monospace" '
               f'font-size="10" fill="{C["chalk"]}">&#129360; Pastry</text>')

    # Counter
    out.append(r(2, 19, 71, 2, C['counter_top']))
    out.append(r(2, 19, 71, 1, C['counter_shine']))
    out.append(r(2, 21, 71, 6, C['counter_face']))
    out.append(r(2, 26, 71, 1, C['counter_top']))
    return out


def build_coffee_machine():
    out = []
    out.append(r(7, 9, 12, 11, C['mach_body']))    # main body
    out.append(r(8, 7, 10, 3, C['mach_dark']))     # top cap
    out.append(r(9, 6, 7, 2, C['mach_dark']))      # hopper
    out.append(r(18, 9, 1, 11, C['mach_shine']))   # right highlight
    out.append(r(9, 10, 5, 4, C['mach_black']))    # display screen
    out.append(r(10, 11, 2, 1, C['mach_green']))   # green LED
    out.append(r(13, 11, 1, 1, C['mach_red']))     # red LED
    out.append(r(10, 13, 2, 1, C['mach_green']))   # green LED 2
    out.append(r(7, 12, 1, 5, C['mach_dark']))     # left panel
    out.append(r(9, 16, 5, 4, C['mach_dark']))     # group head
    out.append(r(10, 18, 3, 2, C['mach_dark']))    # spout
    out.append(r(8, 19, 7, 1, C['mach_dark']))     # drip tray
    return out


def build_machine_steam():
    sx, sy = px(12), px(17)
    return [
        f'<ellipse cx="{sx}" cy="{sy}" rx="4" ry="3" '
        f'fill="{C["mach_steam"]}" class="s1" opacity="0"/>',
        f'<ellipse cx="{sx + 7}" cy="{sy}" rx="3" ry="2" '
        f'fill="{C["mach_steam"]}" class="s2" opacity="0"/>',
        f'<ellipse cx="{sx - 6}" cy="{sy}" rx="3" ry="2" '
        f'fill="{C["mach_steam"]}" class="s3" opacity="0"/>',
    ]


def build_pastry_display():
    out = []
    out.append(r(45, 12, 18, 8, C['case_frame']))   # outer case
    out.append(r(46, 13, 16, 6, C['case_glass']))   # glass front
    out.append(r(47, 16, 14, 1, C['case_shelf']))   # shelf
    # top shelf
    out.append(r(48, 14, 4, 2, C['croissant']))
    out.append(r(49, 13, 2, 1, C['croissant_d']))
    out.append(r(53, 13, 3, 1, C['muffin_top']))
    out.append(r(53, 14, 3, 2, C['muffin']))
    out.append(r(57, 14, 4, 2, C['cookie']))
    # bottom shelf
    out.append(r(48, 17, 3, 2, C['muffin']))
    out.append(r(52, 17, 4, 2, C['croissant']))
    out.append(r(57, 17, 4, 2, C['cookie']))
    return out


def build_barista():
    out = []
    bx = 27
    # hair
    out.append(r(bx, 10, 5, 2, C['bar_hair']))
    # face
    out.append(r(bx, 12, 5, 3, C['bar_skin']))
    out.append(r(bx - 1, 12, 1, 2, C['bar_skin']))   # left ear
    out.append(r(bx + 5, 12, 1, 2, C['bar_skin']))   # right ear
    out.append(r(bx + 1, 13, 1, 1, '#333333'))        # left eye
    out.append(r(bx + 3, 13, 1, 1, '#333333'))        # right eye
    # shirt & apron
    out.append(r(bx, 15, 5, 1, C['bar_shirt']))
    out.append(r(bx - 1, 16, 7, 4, C['bar_apron']))
    out.append(r(bx + 1, 16, 3, 1, C['bar_shirt']))   # apron detail
    # arms
    out.append(r(bx - 2, 17, 2, 2, C['bar_skin']))
    out.append(r(bx + 6, 17, 2, 2, C['bar_skin']))
    return out


def build_customer():
    out = []
    cx = 62
    out.append(r(cx, 12, 5, 2, C['cust_hair']))
    out.append(r(cx, 14, 5, 3, C['cust_skin']))
    out.append(r(cx - 1, 14, 1, 2, C['cust_skin']))   # left ear
    out.append(r(cx + 5, 14, 1, 2, C['cust_skin']))   # right ear
    out.append(r(cx + 1, 15, 1, 1, '#333333'))         # left eye
    out.append(r(cx + 3, 15, 1, 1, '#333333'))         # right eye
    out.append(r(cx - 1, 17, 7, 3, C['cust_shirt']))
    out.append(r(cx, 20, 5, 3, C['cust_pants']))
    out.append(r(cx, 22, 2, 1, '#222222'))              # left shoe
    out.append(r(cx + 3, 22, 2, 1, '#222222'))          # right shoe
    return out


def build_coffee_cup():
    cx = 38
    out = []
    out.append(r(cx, 17, 4, 2, C['cup_body']))         # cup body
    out.append(r(cx, 17, 4, 1, C['cup_coffee']))       # coffee top
    out.append(r(cx, 18, 4, 1, C['cup_sleeve']))       # sleeve
    out.append(r(cx, 17, 4, 1, C['cup_body']))         # rim override
    out.append(r(cx + 4, 18, 1, 1, C['cup_body']))     # handle
    # cup steam
    csx, csy = px(cx + 2), px(16)
    out.append(f'<ellipse cx="{csx}" cy="{csy}" rx="4" ry="3" '
               f'fill="{C["mach_steam"]}" class="s1" opacity="0"/>')
    out.append(f'<ellipse cx="{csx + 7}" cy="{csy}" rx="3" ry="2" '
               f'fill="{C["mach_steam"]}" class="s2" opacity="0"/>')
    return out


def build_pastry_box():
    bx = 40
    out = []
    out.append(r(bx, 17, 5, 2, C['box_body']))         # box body
    out.append(r(bx - 1, 16, 7, 1, C['box_lid']))      # lid
    out.append(r(bx - 1, 17, 7, 1, C['box_ribbon']))   # horizontal ribbon
    out.append(r(bx + 2, 16, 1, 3, C['box_ribbon']))   # vertical ribbon
    out.append(r(bx + 1, 15, 1, 1, C['box_ribbon']))   # bow left
    out.append(r(bx + 3, 15, 1, 1, C['box_ribbon']))   # bow right
    return out


def build_status_bar(state):
    W = px(GW)
    H = px(GH)
    labels = {
        'idle':            "   Welcome! What'll it be?   ",
        'serving_coffee':  "  One coffee, coming right up!  ",
        'serving_pastry':  "    Here's your pastry!    ",
    }
    text = labels.get(state, "")
    return [
        f'<rect x="0" y="{H - 34}" width="{W}" height="34" fill="rgba(0,0,0,0.62)"/>',
        (f'<text x="{W // 2}" y="{H - 11}" font-family="monospace" font-size="13" '
         f'font-weight="bold" fill="white" text-anchor="middle">{text}</text>'),
    ]


def generate(state='idle', order_count=0):
    W, H = px(GW), px(GH)
    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" '
                 f'viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    lines.append(get_styles(state))

    # Static scene
    lines.extend(build_scene())
    lines.extend(build_coffee_machine())
    lines.extend(build_machine_steam())
    lines.extend(build_pastry_display())
    lines.extend(build_barista())

    # State-specific items
    if state == 'serving_coffee':
        lines.append('<g id="cup">')
        lines.extend(build_coffee_cup())
        lines.append('</g>')
    if state == 'serving_pastry':
        lines.append('<g id="box">')
        lines.extend(build_pastry_box())
        lines.append('</g>')

    # Customer (nested groups for independent X/Y animation)
    lines.append('<g id="cx">')   # controls X movement
    lines.append('<g id="cy">')   # controls Y bobbing
    lines.extend(build_customer())
    lines.append('</g>')
    lines.append('</g>')

    # Status bar
    lines.extend(build_status_bar(state))

    lines.append('</svg>')
    return '\n'.join(lines)


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    state_path = os.path.join(script_dir, 'state.json')
    svg_path   = os.path.join(script_dir, 'coffee-shop.svg')

    if os.path.exists(state_path):
        with open(state_path) as f:
            data = json.load(f)
        state = data.get('state', 'idle')
        count = data.get('order_count', 0)
    else:
        state, count = 'idle', 0

    svg = generate(state, count)
    with open(svg_path, 'w') as f:
        f.write(svg)
    print(f"Generated coffee-shop.svg  state={state}  orders={count}")
