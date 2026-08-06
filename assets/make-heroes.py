#!/usr/bin/env python3
"""Generate the repo hero banners.

One script so the five repos share a visual language rather than drifting apart
as each is edited by hand. Run it from anywhere; paths are resolved relative to
the repos directory passed as argv[1] (default: the parent of this file's repo).

Each hero is 1200x300: an eyebrow label, the repo name, one line saying what it
is, a rule, and a footer of the things it contains. The right-hand third carries
a small motif specific to the repo, drawn from the same primitives so they read
as a set.
"""
import os, sys

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"


def head(accent, title, desc):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-label="{title} — {desc}"><title>{title}</title><desc>{desc}</desc><defs><pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0 H0 V28" fill="none" stroke="#101c33" stroke-width="1"/></pattern><radialGradient id="glow"><stop offset="0" stop-color="{accent}" stop-opacity="0.42"/><stop offset="0.55" stop-color="{accent}" stop-opacity="0.10"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient><linearGradient id="hub" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{accent}" stop-opacity="0.55"/><stop offset="1" stop-color="{accent}" stop-opacity="0.15"/></linearGradient></defs><rect width="1200" height="300" fill="#0a0f1a"/><rect width="1200" height="300" fill="url(#grid)" opacity="0.55"/>'''


def text(x, y, s, size, fill, family=MONO, weight=None, anchor=None, spacing=None):
    a = f' font-weight="{weight}"' if weight else ""
    a += f' text-anchor="{anchor}"' if anchor else ""
    a += f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'fill="{fill}"{a}>{s}</text>')


def left(accent, eyebrow, title, subtitle, footer, tsize=40):
    return (f'<circle cx="64" cy="88" r="3.5" fill="{accent}"/>'
            + text(78, 92, eyebrow, 11.5, accent, weight=600, spacing=2.4)
            + text(58, 152, title, tsize, "#f0f6fc", weight=700)
            + text(60, 192, subtitle, 18, "#8c9aab", family=SANS)
            + f'<path d="M60 218 H188" stroke="{accent}" stroke-width="2" opacity="0.7"/>'
            + text(60, 248, footer, 12.5, "#55637a"))


def node(cx, cy, r, accent, fill="#0e1626"):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" '
            f'stroke="{accent}" stroke-width="1.8"/>')


def link(x1, y1, x2, y2, accent, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{accent}" stroke-width="1.4" '
            f'opacity="0.45" fill="none"{d}/>')


def fan_motif(accent, labels):
    """A hub fanning out to N leaves - one thing declared, many places."""
    g = ['<g transform="translate(820,0)">']
    g.append(f'<circle cx="128" cy="150" r="86" fill="url(#glow)"/>')
    n = len(labels)
    for i, lab in enumerate(labels):
        y = 70 + i * (160 / max(n - 1, 1))
        g.append(link(154, 150, 258, y, accent))
        g.append(node(266, y, 5, accent, accent))
        g.append(text(282, y + 4, lab, 12, "#8c9aab"))
    g.append(f'<circle cx="128" cy="150" r="26" fill="url(#hub)" stroke="{accent}" stroke-width="2"/>')
    g.append(text(128, 198, "one source", 10, "#55637a", anchor="middle"))
    g.append("</g>")
    return "".join(g)


def stack_motif(accent, layers):
    """Stacked plates - layers applied in order."""
    g = ['<g transform="translate(830,0)">']
    g.append('<circle cx="150" cy="150" r="96" fill="url(#glow)"/>')
    for i, lab in enumerate(layers):
        y = 78 + i * 42
        g.append(f'<rect x="52" y="{y}" width="200" height="30" rx="6" fill="#0e1626" '
                 f'stroke="{accent}" stroke-width="1.5" opacity="{1 - i*0.16:.2f}"/>')
        g.append(text(68, y + 20, lab, 12, "#8c9aab"))
    g.append("</g>")
    return "".join(g)


def chain_motif(accent, steps):
    """A left-to-right pipeline."""
    g = ['<g transform="translate(770,0)">']
    g.append('<circle cx="190" cy="150" r="100" fill="url(#glow)"/>')
    for i, lab in enumerate(steps):
        x = 60 + i * 110
        if i:
            g.append(link(x - 82, 150, x - 22, 150, accent))
        g.append(node(x, 150, 20, accent))
        g.append(text(x, 154, str(i + 1), 13, accent, anchor="middle", weight=600))
        g.append(text(x, 194, lab, 11, "#8c9aab", anchor="middle"))
    g.append("</g>")
    return "".join(g)


HEROES = {
    "argocd-core": dict(
        accent="#4aa8ff", eyebrow="BOOTSTRAP", tsize=40,
        subtitle="Every deployment in the estate, declared in one values file.",
        footer="projects  ·  clusters  ·  applications  ·  applicationsets",
        motif=lambda a: stack_motif(a, ["argocd", "argocd-app-of-apps", "argocd-config", "argocd-manifests"]),
    ),
    "argocd-app-of-apps": dict(
        accent="#31c48d", eyebrow="RENDERING", tsize=34,
        subtitle="Turns an environment's values into Applications and ApplicationSets.",
        footer="applications  ·  applicationsets  ·  projects  ·  repositories",
        motif=lambda a: fan_motif(a, ["controller", "tooling", "multitenant"]),
    ),
    "argocd-applications": dict(
        accent="#f5a524", eyebrow="CHARTS", tsize=36,
        subtitle="The charts and values the environment files point at.",
        footer="foundational  ·  platform-engineering  ·  security",
        motif=lambda a: stack_motif(a, ["foundational/", "platform-engineering/", "security/"]),
    ),
    "helm-library-manifests": dict(
        accent="#a672ff", eyebrow="LIBRARY", tsize=30,
        subtitle="The manifests every application repeats, as values instead of copies.",
        footer="externalsecrets  ·  certificates  ·  tls-proxies  ·  configmaps",
        motif=lambda a: fan_motif(a, ["externalSecrets", "certificates", "tlsProxies", "customResources"]),
    ),
    "platform-agent-stack": dict(
        accent="#a672ff", eyebrow="ORCHESTRATION", tsize=34,
        subtitle="Agent topology, risk policy and pluggable backends in one repo.",
        footer="swarm  ·  policy  ·  itsm  ·  llm  ·  chat",
        motif=lambda a: chain_motif(a, ["classify", "decide", "execute"]),
    ),
}


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..")
    for repo, cfg in HEROES.items():
        d = os.path.join(root, repo, "assets")
        if not os.path.isdir(os.path.join(root, repo)):
            print(f"  skip {repo} (not checked out)")
            continue
        os.makedirs(d, exist_ok=True)
        a = cfg["accent"]
        svg = (head(a, repo, cfg["subtitle"])
               + cfg["motif"](a)
               + left(a, cfg["eyebrow"], repo, cfg["subtitle"], cfg["footer"], cfg["tsize"])
               + "</svg>")
        with open(os.path.join(d, "hero.svg"), "w") as f:
            f.write(svg)
        print(f"  wrote {repo}/assets/hero.svg ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
