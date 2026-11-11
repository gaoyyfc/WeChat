"""Build saved, complete image prompts from the reviewed topic-specific content."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

COMMON = """Create ONE original finished Chinese WeChat image-post card. Portrait 1152×1536, 3:4. This is publication-ready editorial content for middle-aged adults, not a webpage, app UI, screenshot, comic or slide deck.

LAYOUT: outer margins 90 px or more on all sides; consistent left-aligned editorial grid. Clean composition with generous white space. Simple background. Main elements positioned by content needs. Keep title, content and footer clearly separated. All content must stay inside the canvas. Main title usually 92–112 px, content 54–64 px, small supporting text at least 44 px, page number 38 px. Strong practical readability at 360 px phone width matters more than decorative details. Wrap long sentences instead of shrinking type. Use plain legible Chinese sans-serif, not hard-to-read calligraphy.

REFERENCE ROLES: reference inputs provide hierarchy, visual pacing and composition ONLY. Never reproduce their subject, words, layout exactly, screenshots, brands, UI controls, icons or watermarks. If a series cover is the FIRST reference, match that series' typography, palette, margins, visual texture and photographic treatment; change the page layout and visible words according to the instructions. Source photos are mood references only; make entirely new original everyday scenes. Do not duplicate their people, location, framing or identifiable elements.

CONSTRAINTS: all people-free. Ordinary objects and settings only. No cartoon, manga, exaggerated characters, AI fantasy, glossy 3D render, luxury interior, dramatic cinematic lighting, busy decoration, ornamental badges, sparkles, fake stamps, fake brand endorsement, fake invoice, fake chat UI, battery icon, medical icon, company logo, QR code or watermark. No dates or statistics, no fabricated facts. Avoid tiny words, heavy paper grain and dark textured backgrounds. All visible Chinese must be exact, complete, not garbled and not cropped. Technical colors and English instructions are NEVER visible labels. The supplied LABELS are the only visible text, excluding pure shapes.
"""

LAYOUTS = {
    "cover": """ZONES: small eyebrow at y=105; four-line very bold hero headline from y=310 to y=990, 116–126 px. One sage note-paper layer offsets behind the title without reducing contrast. Subtitle y=1150, 48 px, may wrap. Tiny topic-specific still-life near bottom, subordinate to headline. Page number bottom right. Calm, inviting and spacious, not a busy scrapbook.""",
    "two-notes": """ZONES: eyebrow at y=100; two-line strong headline y=220. Two roomy paper-note panels stacked from y=550 to y=1200, one per LABELS block. Each panel has a 54 px bold short label and 56–60 px text below, ample padding. Flat paper layers and fine lines, not dense boxes. Takeaway at y=1330 in 44 px, may wrap. Page number lower right. Tiny object photos may sit at panel corners, away from text.""",
    "three-rows": """ZONES: eyebrow y=100; two-line headline y=210, 92–100 px. Three generously spaced rows between y=550 and y=1210. Each row has a short 54 px bold sage-backed label and one or two lines of 56 px text. Thin separator rules or tiny sage tabs. Takeaway y=1330, 42–44 px, may wrap into two lines. Tiny still-life allowed only at a corner without constricting text. Page number lower right.""",
    "quotes": """ZONES: eyebrow y=100, two-line large title y=210. Two spacious quote-note panels centered between y=570 and y=1200. Each has a short 50 px label outside the panel and the reply in 60 px clear type, two lines with 85 px line spacing. Minimal sage paper treatment, subtle quote corners, no real chat UI. Takeaway y=1330, 44 px, may wrap. Page number lower right.""",
    "photo-cover": """ZONES: upper 62% linen-white editorial zone, lower 38% original natural lifestyle photograph. Small eyebrow y=100. Four-line hero headline y=250 to y=850, 114–124 px, highest priority. One subtle dusk-blue underline or block only. Subtitle y=925, 46–50 px. Photo starts around y=1000 and bleeds to bottom, with natural quiet composition and no text printed inside photograph. Page number stays in editorial zone or inside a small clean white footer. No dark gradients, no photo filter overlay behind text.""",
    "photo-notes": """ZONES: top linen-white 70% contains eyebrow y=95, two-line headline y=200, two airy text blocks from y=510 to y=970. Each block has a 52 px label and 54–60 px body; muted blue short labels, not cards crowded together. A new original lifestyle photo strip from y=1030 to y=1340 shows the exact objects below. Takeaway on white at y=1390, 40–44 px, may wrap. Page number discreet lower right. Photo and text share the same soft blue/linen/warm-light treatment as the cover.""",
    "photo-rows": """ZONES: eyebrow y=95, two-line headline y=200, three compact but airy text rows y=500 to y=960. Each row: a 50–52 px bold label, then 54–58 px body. No decorative note overlays on text. A new original photo strip y=1010 to y=1330, exact scene specified below. Takeaway on white at y=1390, 40–44 px, may wrap. Page number discreet lower right. Keep linen-white background and dusk-blue tabs from cover.""",
    "recovery-checklist": """ZONES: eyebrow y=95, two-line headline y=200. Four widely spaced rows y=530 to y=1240. Each row: 50–54 px bold blue-backed short label, followed by 54–58 px body, no checkbox pressure or progress tracker. A tiny everyday-object photo may occupy an empty corner, never behind words. Takeaway y=1370, 42–44 px on white, may wrap; no alarming styling. Page number lower right.""",
    "repair-cover": """ZONES: eyebrow y=100. Huge three-line practical headline y=330 to y=930, 130–142 px. Highlight ONLY the 5 or 5句话 with orange, maintaining dark navy text contrast. Subtitle y=1090, 50–56 px. Original generic tool still-life at bottom right, no more than 22% of page. Page number lower right. Headline dominates; this is a useful service checklist rather than a warning billboard. No extra decorative 5 outside the title.""",
    "question": """ZONES: top eyebrow left, small orange number tab on right around y=100. Strong two-line headline at y=240, 96–106 px. One central off-white or pale-blue quote panel y=590 to y=890 with a thin orange edge; quote at 58–64 px with broad padding, may use up to three lines. Under it, detail in 50–54 px, y=1000 to y=1190, two or three lines. Takeaway y=1340, 44 px, may wrap. One tiny object photo near lower margin if room. Page number lower right. All questions and detail lines legible. Number tab is the question number, distinct from page number.""",
    "repair-checklist": """ZONES: eyebrow y=90; two-line headline y=190, 96–104 px. Five roomy ruled rows from y=495 to y=1260, one per block. Each row has 48–50 px bold label containing an orange question number, and 52–54 px body immediately below it. Each reply fits one line or at most two, no microscopic text. No photo or extra ornament. Takeaway y=1380 in 42 px, may wrap. Page number bottom right. This is a screenshot-friendly summary tool.""",
}


def main():
    for item in json.loads((HERE / "选题制作清单.json").read_text()):
        folder = HERE / item["slug"]
        topic = json.loads((folder / "制作内容.json").read_text())
        for index, card in enumerate(topic["cards"], 1):
            if index == 1:
                references = topic["references"]
            else:
                references = []
                if (folder / "references/00-本组封面.png").exists():
                    references.append("00-本组封面.png")
                references.append(topic["references"][-1])
            labels = {"eyebrow": topic["eyebrow"], "title": card["title"]}
            for key in ("subtitle", "number", "quote", "detail", "blocks", "takeaway"):
                if key in card:
                    labels[key] = card[key]
            labels["page"] = f"{index:02d} / {len(topic['cards']):02d}"
            frontmatter = f"---\nillustration_id: {index:02d}\ntype: {card['layout']}\nstyle: topic-specific-editorial\nlanguage: zh\nreferences:\n"
            for n, ref in enumerate(references, 1):
                assert (folder / "references" / ref).exists()
                frontmatter += f"  - ref_id: ref-{n}\n    filename: {ref}\n    usage: direct\n"
            frontmatter += "---\n\n"
            prompt = frontmatter + COMMON + "\nSTYLE: " + topic["style"]
            prompt += "\n\nCOLORS: " + json.dumps(topic["palette"], ensure_ascii=False)
            prompt += "\nColor values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, JSON keys or palette labels as visible text. Accent fills remain soft so dark text has strong contrast.\n\n"
            prompt += LAYOUTS[card["layout"]]
            prompt += "\n\nVISUAL MATERIAL: " + card["visual"]
            prompt += "\n\nLABELS — ONLY the following strings are visible; render the values in Chinese, not JSON keys. Respect line breaks and do not add content:\n"
            prompt += json.dumps(labels, ensure_ascii=False, indent=2)
            prompt += "\n\nASPECT: 3:4. Finished single raster image, not a grid of multiple cards.\n"
            if card.get("revision_geometry"):
                prompt += "\nREVISION — GEOMETRY PRIORITY: " + card["revision_geometry"] + "\n"
            (folder / "prompts" / f"{card['id']}.md").write_text(prompt)
    print("Saved all 19 complete prompts; references validated.")


if __name__ == "__main__":
    main()
