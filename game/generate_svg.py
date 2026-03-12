#!/usr/bin/env python3
"""Generate idle.svg, serve-coffee.svg, and serve-pastry.svg for the coffee shop README."""
import os

U  = 8        # px per grid unit
GW = 75       # grid width  → 600 px
GH = 34       # grid height → 272 px

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
    'steam':        '#DDDDDD',
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


def px(v):
    return v * U


def r(x, y, w, h, c, **kw):
    attrs = ''.join(f' {k}="{v}"' for k, v in kw.items())
    return f'<rect x="{px(x)}" y="{px(y)}" width="{px(w)}" height="{px(h)}" fill="{c}"{attrs}/>'


def txt(x, y, s, size, color, anchor='start', weight='normal'):
    return (f'<text x="{px(x)}" y="{px(y)}" font-family="monospace" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{s}</text>')


# ── Static scene pieces ────────────────────────────────────────────────────────

def scene_background():
    out = []
    out.append(r(0, 0, GW, 21, C['wall']))
    for col in range(0, GW, 12):
        out.append(r(col, 0, 1, 21, C['wall_stripe']))
    out.append(r(0, 21, GW, GH - 21, C['floor']))
    for fy in range(21, GH, 3):
        out.append(r(0, fy, GW, 1, C['floor_dark']))
    return out


def scene_window():
    out = []
    out.append(r(3, 1, 22, 17, C['win_frame']))
    out.append(r(4, 2, 20, 15, C['win_sky']))
    out.append(r(6, 3,  5,  2, C['win_cloud']))
    out.append(r(14, 4, 6,  2, C['win_cloud']))
    out.append(r(10, 5, 3,  1, C['win_cloud']))
    out.append(r(14, 2, 1, 15, C['win_frame']))   # vertical divider
    out.append(r(4,  10, 20, 1, C['win_frame']))  # horizontal divider
    out.append(r(2,  18, 24, 1, C['win_frame']))  # sill
    return out


def scene_menu_board():
    out = []
    out.append(r(50, 1, 24,  1, C['board_trim']))
    out.append(r(50, 1, 24, 14, C['board']))
    out.append(r(50, 14, 24, 1, C['board_trim']))
    out.append(r(50,  1,  1, 14, C['board_trim']))
    out.append(r(73,  1,  1, 14, C['board_trim']))
    out.append(txt(62, 5, 'MENU', 12, C['chalk_yellow'], 'middle', 'bold'))
    out.append(f'<line x1="{px(51)}" y1="{px(6)}" x2="{px(73)}" y2="{px(6)}" '
               f'stroke="{C["chalk_dim"]}" stroke-width="1"/>')
    out.append(txt(53,  9, '&#9749; Coffee', 10, C['chalk']))
    out.append(txt(53, 12, '&#129360; Pastry', 10, C['chalk']))
    return out


def scene_counter():
    out = []
    out.append(r(2, 19, 71, 2, C['counter_top']))
    out.append(r(2, 19, 71, 1, C['counter_shine']))
    out.append(r(2, 21, 71, 5, C['counter_face']))
    out.append(r(2, 25, 71, 1, C['counter_top']))
    return out


def scene_coffee_machine():
    out = []
    out.append(r(7,  9, 12, 11, C['mach_body']))
    out.append(r(8,  7, 10,  3, C['mach_dark']))
    out.append(r(9,  6,  7,  2, C['mach_dark']))
    out.append(r(18, 9,  1, 11, C['mach_shine']))
    out.append(r(9, 10,  5,  4, C['mach_black']))
    out.append(r(10, 11, 2,  1, C['mach_green']))
    out.append(r(13, 11, 1,  1, C['mach_red']))
    out.append(r(10, 13, 2,  1, C['mach_green']))
    out.append(r(7,  12, 1,  5, C['mach_dark']))
    out.append(r(9,  16, 5,  4, C['mach_dark']))   # group head
    out.append(r(10, 18, 3,  2, C['mach_dark']))   # spout
    out.append(r(8,  19, 7,  1, C['mach_dark']))   # drip tray
    return out


def scene_pastry_display():
    out = []
    out.append(r(45, 12, 18,  8, C['case_frame']))
    out.append(r(46, 13, 16,  6, C['case_glass']))
    out.append(r(47, 16, 14,  1, C['case_shelf']))
    # top shelf
    out.append(r(48, 14,  4,  2, C['croissant']))
    out.append(r(49, 13,  2,  1, C['croissant_d']))
    out.append(r(53, 13,  3,  1, C['muffin_top']))
    out.append(r(53, 14,  3,  2, C['muffin']))
    out.append(r(57, 14,  4,  2, C['cookie']))
    # bottom shelf
    out.append(r(48, 17,  3,  2, C['muffin']))
    out.append(r(52, 17,  4,  2, C['croissant']))
    out.append(r(57, 17,  4,  2, C['cookie']))
    return out


def scene_barista():
    bx = 27
    out = []
    out.append(r(bx,      10,  5,  2, C['bar_hair']))
    out.append(r(bx,      12,  5,  3, C['bar_skin']))
    out.append(r(bx - 1,  12,  1,  2, C['bar_skin']))
    out.append(r(bx + 5,  12,  1,  2, C['bar_skin']))
    out.append(r(bx + 1,  13,  1,  1, '#444444'))
    out.append(r(bx + 3,  13,  1,  1, '#444444'))
    out.append(r(bx,      15,  5,  1, C['bar_shirt']))
    out.append(r(bx - 1,  16,  7,  4, C['bar_apron']))
    out.append(r(bx + 1,  16,  3,  1, C['bar_shirt']))
    out.append(r(bx - 2,  17,  2,  2, C['bar_skin']))
    out.append(r(bx + 6,  17,  2,  2, C['bar_skin']))
    return out


def customer_pixels(cx=62):
    """Customer sprite at grid x = cx."""
    out = []
    out.append(r(cx,      12,  5,  2, C['cust_hair']))
    out.append(r(cx,      14,  5,  3, C['cust_skin']))
    out.append(r(cx - 1,  14,  1,  2, C['cust_skin']))
    out.append(r(cx + 5,  14,  1,  2, C['cust_skin']))
    out.append(r(cx + 1,  15,  1,  1, '#444444'))
    out.append(r(cx + 3,  15,  1,  1, '#444444'))
    out.append(r(cx - 1,  17,  7,  3, C['cust_shirt']))
    out.append(r(cx,      20,  5,  3, C['cust_pants']))
    out.append(r(cx,      22,  2,  1, '#222222'))
    out.append(r(cx + 3,  22,  2,  1, '#222222'))
    return out


def machine_steam_els():
    sx, sy = px(12), px(17)
    return [
        f'<ellipse cx="{sx}"     cy="{sy}" rx="4" ry="3" fill="{C["steam"]}" class="s1" opacity="0"/>',
        f'<ellipse cx="{sx + 7}" cy="{sy}" rx="3" ry="2" fill="{C["steam"]}" class="s2" opacity="0"/>',
        f'<ellipse cx="{sx - 6}" cy="{sy}" rx="3" ry="2" fill="{C["steam"]}" class="s3" opacity="0"/>',
    ]


def cup_steam_els(cx=38):
    sx, sy = px(cx + 2), px(17)
    return [
        f'<ellipse cx="{sx}"     cy="{sy}" rx="4" ry="3" fill="{C["steam"]}" class="cs1" opacity="0"/>',
        f'<ellipse cx="{sx + 7}" cy="{sy}" rx="3" ry="2" fill="{C["steam"]}" class="cs2" opacity="0"/>',
    ]


def coffee_cup_els(cx=38):
    out = []
    out.append(r(cx,     17,  4,  2, C['cup_body']))
    out.append(r(cx,     17,  4,  1, C['cup_coffee']))
    out.append(r(cx,     18,  4,  1, C['cup_sleeve']))
    out.append(r(cx,     17,  4,  1, C['cup_body']))   # rim
    out.append(r(cx + 4, 18,  1,  1, C['cup_body']))   # handle
    return out


def pastry_box_els(bx=40):
    out = []
    out.append(r(bx,     17,  5,  2, C['box_body']))
    out.append(r(bx - 1, 16,  7,  1, C['box_lid']))
    out.append(r(bx - 1, 17,  7,  1, C['box_ribbon']))
    out.append(r(bx + 2, 16,  1,  3, C['box_ribbon']))
    out.append(r(bx + 1, 15,  1,  1, C['box_ribbon']))
    out.append(r(bx + 3, 15,  1,  1, C['box_ribbon']))
    return out


def status_bar(text):
    W, H = px(GW), px(GH)
    return [
        f'<rect x="0" y="{H - 32}" width="{W}" height="32" fill="rgba(0,0,0,0.62)"/>',
        (f'<text x="{W // 2}" y="{H - 10}" font-family="monospace" font-size="13" '
         f'font-weight="bold" fill="white" text-anchor="middle">{text}</text>'),
    ]


def svg_wrap(styles, body_lines):
    W, H = px(GW), px(GH)
    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    lines.append(styles)
    lines.extend(body_lines)
    lines.append('</svg>')
    return '\n'.join(lines)


# ── Per-state SVG generators ───────────────────────────────────────────────────

def generate_idle():
    styles = """<style>
  @keyframes walk-in {
    0%   { transform: translateX(192px); }
    70%  { transform: translateX(0); }
    100% { transform: translateX(0); }
  }
  @keyframes bob {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-4px); }
  }
  @keyframes steam {
    0%   { opacity: 0; transform: translateY(0) scale(1); }
    40%  { opacity: 0.8; }
    100% { opacity: 0; transform: translateY(-28px) scale(1.4); }
  }
  .s1 { animation: steam 2.6s ease-out infinite; }
  .s2 { animation: steam 2.6s ease-out 0.9s infinite; }
  .s3 { animation: steam 2.6s ease-out 1.7s infinite; }
  #cx { animation: walk-in 1.8s cubic-bezier(.15,.85,.35,1) forwards; }
  #cy { animation: bob 1.1s ease-in-out 1.8s infinite; }
</style>"""

    body = []
    body.extend(scene_background())
    body.extend(scene_window())
    body.extend(scene_menu_board())
    body.extend(scene_counter())
    body.extend(scene_coffee_machine())
    body.extend(machine_steam_els())
    body.extend(scene_pastry_display())
    body.extend(scene_barista())

    body.append('<g id="cx"><g id="cy">')
    body.extend(customer_pixels())
    body.append('</g></g>')

    body.extend(status_bar("  Welcome! What\u2019ll it be?  "))
    return svg_wrap(styles, body)


def generate_serve_coffee():
    styles = """<style>
  @keyframes bob {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-3px); }
  }
  @keyframes lean {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-10px); }
  }
  @keyframes cup-rise {
    0%   { transform: translateY(20px); opacity: 0; }
    50%  { transform: translateY(0);    opacity: 1; }
    100% { transform: translateY(0);    opacity: 1; }
  }
  @keyframes steam {
    0%   { opacity: 0; transform: translateY(0) scale(1); }
    40%  { opacity: 0.8; }
    100% { opacity: 0; transform: translateY(-28px) scale(1.4); }
  }
  /* machine steam: 2 puffs then done */
  .s1 { animation: steam 2.6s ease-out 2; }
  .s2 { animation: steam 2.6s ease-out 0.9s 2; }
  .s3 { animation: steam 2.6s ease-out 1.7s 1; }
  /* cup steam: loops after cup arrives */
  .cs1 { animation: steam 2s ease-out 1s infinite; }
  .cs2 { animation: steam 2s ease-out 1.8s infinite; }
  #cx { animation: lean 0.7s ease-out 0.3s forwards; }
  #cy { animation: bob 1.1s ease-in-out infinite; }
  #cup { animation: cup-rise 0.8s ease-out forwards; }
</style>"""

    body = []
    body.extend(scene_background())
    body.extend(scene_window())
    body.extend(scene_menu_board())
    body.extend(scene_counter())
    body.extend(scene_coffee_machine())
    body.extend(machine_steam_els())
    body.extend(scene_pastry_display())
    body.extend(scene_barista())

    # Cup + its steam
    body.append('<g id="cup">')
    body.extend(coffee_cup_els())
    body.append('</g>')
    body.extend(cup_steam_els())

    body.append('<g id="cx"><g id="cy">')
    body.extend(customer_pixels())
    body.append('</g></g>')

    body.extend(status_bar("  \u2615 One coffee, coming right up!  "))
    return svg_wrap(styles, body)


def generate_serve_pastry():
    styles = """<style>
  @keyframes bob {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-3px); }
  }
  @keyframes lean {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-10px); }
  }
  @keyframes box-arrive {
    0%   { transform: translateX(-56px); opacity: 0; }
    65%  { transform: translateX(4px);   opacity: 1; }
    80%  { transform: translateX(-2px);  opacity: 1; }
    100% { transform: translateX(0);     opacity: 1; }
  }
  @keyframes steam {
    0%   { opacity: 0; transform: translateY(0) scale(1); }
    40%  { opacity: 0.8; }
    100% { opacity: 0; transform: translateY(-28px) scale(1.4); }
  }
  .s1 { animation: steam 2.6s ease-out 1; }
  .s2 { animation: steam 2.6s ease-out 0.9s 1; }
  .s3 { animation: steam 2.6s ease-out 0; }
  #cx { animation: lean 0.7s ease-out 0.3s forwards; }
  #cy { animation: bob 1.1s ease-in-out infinite; }
  #box { animation: box-arrive 0.9s ease-out 0.1s both; }
</style>"""

    body = []
    body.extend(scene_background())
    body.extend(scene_window())
    body.extend(scene_menu_board())
    body.extend(scene_counter())
    body.extend(scene_coffee_machine())
    body.extend(machine_steam_els())
    body.extend(scene_pastry_display())
    body.extend(scene_barista())

    body.append('<g id="box">')
    body.extend(pastry_box_els())
    body.append('</g>')

    body.append('<g id="cx"><g id="cy">')
    body.extend(customer_pixels())
    body.append('</g></g>')

    body.extend(status_bar("  \U0001f950 Here\u2019s your pastry!  "))
    return svg_wrap(styles, body)


# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    out_dir = os.path.dirname(os.path.abspath(__file__))
    for filename, svg in [
        ('idle.svg',          generate_idle()),
        ('serve-coffee.svg',  generate_serve_coffee()),
        ('serve-pastry.svg',  generate_serve_pastry()),
    ]:
        path = os.path.join(out_dir, filename)
        with open(path, 'w') as f:
            f.write(svg)
        print(f"Generated {filename}")
