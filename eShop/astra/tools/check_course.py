"""Validate Astra's local navigation and story structure; no third-party packages.

Run from the eShop root: python astra/tools/check_course.py
This checks documentation structure, not application behavior or external URLs.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

COURSE = Path(__file__).resolve().parents[1]
EXPECTED = {f"ASTRA-{number:03}" for number in range(1, 73)}
REQUIRED = (
    "User story",
    "Starting point and scope",
    "Acceptance criteria",
    "Suggested approach",
    "Verification and evidence",
    "Hints, in order",
    "Review conversation",
)
errors = []
files = sorted(COURSE.rglob("*.md"))
links_checked = 0

def without_fences(text):
    lines = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(line)
    return "\n".join(lines)

for path in files:
    text = path.read_text(encoding="utf-8")
    visible = without_fences(text)
    if not visible.startswith("# "):
        errors.append(f"{path.relative_to(COURSE)}: missing top-level title")
    if sum(line.lstrip().startswith("```") for line in text.splitlines()) % 2:
        errors.append(f"{path.relative_to(COURSE)}: unbalanced code fences")
    for destination in re.findall(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", visible):
        destination = destination.strip().strip("<>")
        parsed = urlsplit(destination)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = (path.parent / unquote(parsed.path)).resolve()
        links_checked += 1
        if not target.exists():
            errors.append(f"{path.relative_to(COURSE)}: missing target {destination}")
        if parsed.fragment:
            errors.append(f"{path.relative_to(COURSE)}: anchor verification unsupported: {destination}")

story_files = sorted((COURSE / "02-stories").glob("ASTRA-*.md"))
actual = {path.stem for path in story_files}
if actual != EXPECTED:
    errors.append(f"Story IDs differ: missing={sorted(EXPECTED-actual)}, extra={sorted(actual-EXPECTED)}")
index = (COURSE / "02-stories" / "README.md").read_text(encoding="utf-8")
tracker = (COURSE / "PROGRESS.md").read_text(encoding="utf-8")

for path in story_files:
    text = path.read_text(encoding="utf-8")
    story_id = path.stem
    if not text.startswith(f"# {story_id}: "):
        errors.append(f"{story_id}: title mismatch")
    for heading in REQUIRED:
        if f"## {heading}\n" not in text:
            errors.append(f"{story_id}: missing section {heading}")
    acceptance = re.search(r"## Acceptance criteria\n(.*?)(?=\n## )", text, re.S)
    if not acceptance or len(re.findall(r"^- \[ \] ", acceptance.group(1), re.M)) < 3:
        errors.append(f"{story_id}: fewer than three acceptance criteria")
    dependency_line = re.search(r"\*\*Prerequisites:\*\* ([^\n]+)", text)
    if not dependency_line:
        errors.append(f"{story_id}: missing prerequisites")
    else:
        for dep in set(re.findall(r"ASTRA-\d{3}", dependency_line.group(1))):
            if dep not in EXPECTED or dep >= story_id:
                errors.append(f"{story_id}: invalid/non-earlier prerequisite {dep}")
    stage = (int(story_id[-3:]) - 1) // 6 + 1
    if not re.search(rf"\*\*Stage:\*\* {stage} ", text):
        errors.append(f"{story_id}: wrong stage")
    if f"[{story_id}]({story_id}.md)" not in index:
        errors.append(f"{story_id}: missing index link")
    if f"[{story_id}](02-stories/{story_id}.md)" not in tracker:
        errors.append(f"{story_id}: missing progress row")

if errors:
    print("\n".join(errors))
    print(f"FAILED: {len(errors)} issue(s)")
    sys.exit(1)
words = sum(len(re.findall(r"\b[\w'-]+\b", p.read_text(encoding="utf-8"))) for p in files)
print(f"PASS: {len(files)} Markdown files, {len(story_files)} stories, {links_checked} local links.")
print(f"Story structure, prerequisite ordering, index, and tracker verified. Approximate words: {words}.")
