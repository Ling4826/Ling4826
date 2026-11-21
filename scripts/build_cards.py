"""Build the game-style SVG cards for the profile README.

  python scripts/build_cards.py cards          -> assets/cards/*.svg (static, commit them)

Every card has a viewBox and its own light background, so it scales to any
screen width and looks the same in GitHub's light and dark themes.
"""
import base64, os, sys
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER = "Ling4826"
FONT = "font-family=\"'Segoe UI','Helvetica Neue',Arial,sans-serif\""
INK, SUB, LINE = "#24496b", "#5f7f99", "#cfe6f5"
VO, DA, VI = "#f2507e", "#2e9bea", "#f5b02e"


def img64(rel):
    with open(os.path.join(ROOT, rel), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT} role="img">'
            f'<title>{escape(title)}</title>{body}</svg>\n')


def sparkle(x, y, s, delay, color="#ffffff"):
    p = f"M0,-{s} Q{s*.18},-{s*.18} {s},0 Q{s*.18},{s*.18} 0,{s} Q-{s*.18},{s*.18} -{s},0 Q-{s*.18},-{s*.18} 0,-{s}Z"
    return (f'<path d="{p}" fill="{color}" transform="translate({x},{y})" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;0" dur="2.4s" begin="{delay}s" repeatCount="indefinite"/></path>')


def panel(w, h, label, color=INK):
    return (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>'
            f'<path d="M1,19 a18,18 0 0 1 18,-18 h{w-38} a18,18 0 0 1 18,18 v25 h-{w-2}z" fill="#eef7fd"/>'
            f'<rect x="22" y="14" width="6" height="18" rx="3" fill="{color}"/>'
            f'<text x="38" y="29" font-size="15" font-weight="800" letter-spacing="2" fill="{INK}">{escape(label)}</text>')


def header():
    w, h = 800, 280
    stripes = "".join(f'<rect x="{x}" y="-40" width="18" height="400" fill="#ffffff" opacity=".12" transform="rotate(25 {x} 0)"/>' for x in range(-100, 900, 60))
    stars = "".join(sparkle(x, y, s, d) for x, y, s, d in [(60, 50, 9, 0), (300, 40, 6, .8), (470, 70, 8, 1.6), (520, 220, 6, .4), (40, 230, 7, 1.2), (380, 245, 5, 2)])
    body = f'''<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4fbff"/><stop offset=".55" stop-color="#cbe9f8"/><stop offset="1" stop-color="#8fcdee"/></linearGradient>
<clipPath id="c"><rect width="{w}" height="{h}" rx="22"/></clipPath></defs>
<g clip-path="url(#c)"><rect width="{w}" height="{h}" fill="url(#bg)"/>{stripes}
<circle cx="640" cy="150" r="150" fill="#ffffff" opacity=".35"/>
<image href="{img64('assets/lilja.png')}" x="500" y="-6" width="300" height="300" preserveAspectRatio="xMidYMin meet"/>
{stars}
<text x="44" y="70" font-size="14" font-weight="700" letter-spacing="3" fill="{SUB}">HATSUBOSHI GAKUEN · PRODUCE REPORT</text>
<text x="40" y="142" font-size="78" font-weight="900" fill="#ffffff" stroke="{INK}" stroke-width="10" paint-order="stroke" stroke-linejoin="round">LingTH</text>
<text x="44" y="182" font-size="19" font-weight="700" fill="{INK}">Software Engineering Course · Year 3</text>
<text x="44" y="207" font-size="15" fill="{SUB}">CAMT, Chiang Mai University</text>
<rect x="44" y="224" width="372" height="34" rx="17" fill="{VO}"/>
<text x="230" y="247" font-size="15" font-weight="800" fill="#ffffff" text-anchor="middle">NOW AUDITIONING · Summer 2027 intern</text>
</g>'''
    return svg(w, h, body, "LingTH produce report")


def parameters():
    w, h = 800, 300
    rows = [("Vo", "Backend", VO, .8, "NestJS · Java Spring Boot · PostgreSQL · TypeORM"),
            ("Da", "Frontend", DA, .7, "Next.js · Vue 3 · TypeScript"),
            ("Vi", "DevOps", VI, .6, "Docker · Nginx · Portainer · Jest")]
    body = panel(w, h, "PARAMETERS")
    bar_x, bar_w = 210, 540
    for i, (tag, name, col, frac, skills) in enumerate(rows):
        y = 78 + i * 72
        body += f'''<circle cx="56" cy="{y+14}" r="22" fill="{col}"/><text x="56" y="{y+21}" font-size="19" font-weight="900" fill="#fff" text-anchor="middle">{tag}</text>
<text x="92" y="{y+22}" font-size="24" font-weight="800" fill="{INK}">{name}</text>
<rect x="{bar_x}" y="{y+4}" width="{bar_w}" height="20" rx="10" fill="#edf3f8"/>
<rect x="{bar_x}" y="{y+4}" width="{bar_w*frac:.0f}" height="20" rx="10" fill="{col}"><animate attributeName="width" from="0" to="{bar_w*frac:.0f}" dur="1.2s" begin="{.2+i*.25}s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect>
<rect x="{bar_x+6}" y="{y+7}" width="{bar_w*frac-12:.0f}" height="5" rx="2.5" fill="#fff" opacity=".45"><animate attributeName="width" from="0" to="{bar_w*frac-12:.0f}" dur="1.2s" begin="{.2+i*.25}s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect>
<text x="{bar_x}" y="{y+50}" font-size="18" fill="{SUB}">{escape(skills)}</text>'''
    body += f'<image href="{img64("assets/items/parameters.png")}" x="{w-74}" y="-4" width="60" height="60"/>'
    return svg(w, h, body, "Parameters: Backend, Frontend, DevOps")


LIVES = [
    ("arcana", "ARCANA", "Coding exam platform · paid student developer at CAMT", VO, "LIVE",
     ["The college ran a full semester of exams on it.", "446 of 447 commits are mine · NestJS, Next.js, Docker"]),
    ("memory-clip", "MEMORY CLIP", "Wearable ESP32-S3 camera + Flask server · solo", DA, "SOLO",
     ["5 days of real use: 2,861 photos and 60 clips.", "Deep sleep firmware, AI captions, daily highlight video"]),
    ("ridee", "RIDEE", "AI eco-ride score · K-CAMT 2026 Climate Tech Hackathon", VI, "3RD",
     ["3rd place. Led a Thai-Korean team.", "Live ride simulation on real roads, fleet impact dashboard"]),
    ("ai-not-pass", "AI NOT PASS", "Spring Boot + Vue · SE331 team of 3", VO, "TEAM",
     ["Members pass level exams to unlock AI services.", "JWT login with refresh and revocation, role-based access"]),
    ("artistverse", "ARTISTVERSE X", "Vue 3 + Flask · music app", DA, "TEAM",
     ["Recommends songs from Spotify and writes lyrics with AI.", ""]),
]


def live(key, title, sub, col, badge, lines):
    w, h = 800, 178
    body = (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>'
            f'<path d="M1,19 a18,18 0 0 1 18,-18 h12 v{h-2} h-12 a18,18 0 0 1 -18,-18z" fill="{col}"/>'
            f'<text x="56" y="50" font-size="32" font-weight="900" fill="{INK}" letter-spacing="1">{escape(title)}</text>'
            f'<text x="56" y="82" font-size="19" font-weight="700" fill="{col}">{escape(sub)}</text>')
    for i, t in enumerate(lines):
        if t:
            body += f'<text x="56" y="{118+i*28}" font-size="20" fill="{SUB}">{escape(t)}</text>'
    body += (f'<g transform="translate({w-70},{h/2})"><circle r="40" fill="{col}" opacity=".12"/>'
             f'<circle r="31" fill="#fff" stroke="{col}" stroke-width="4"/>'
             f'<text y="7" font-size="{20 if len(badge) <= 3 else 16}" font-weight="900" fill="{col}" text-anchor="middle">{badge}</text>'
             f'<animateTransform attributeName="transform" type="scale" additive="sum" values="1;1.06;1" dur="2s" repeatCount="indefinite"/></g>')
    return svg(w, h, body, f"{title}: {sub}")




if __name__ == "__main__":
    if sys.argv[1] == "cards":
        out = os.path.join(ROOT, "assets", "cards")
        os.makedirs(out, exist_ok=True)
        files = {"header.svg": header(), "parameters.svg": parameters()}
        files.update({f"live-{k}.svg": live(k, *rest) for k, *rest in LIVES})
        for name, text in files.items():
            with open(os.path.join(out, name), "w", encoding="utf-8") as f:
                f.write(text)
        print("wrote", ", ".join(files))
