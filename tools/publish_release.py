#!/usr/bin/env python3
"""Publish the manufacturing files of every board's current release as a GitHub release (docs/decisions.md D-22).

For each edakit project of the repository (edakit.toml at the root, variants/*/edakit.toml) the script takes the
current release from `edakit release current`, lets `edakit release verify` check the order files against it, copies
them with the polarity picture and the manifest into build/publish/<tag>/, writes SHA256SUMS and the release notes,
and creates the release with `gh release create --prerelease`. The tag is the date; the pre-release mark stays until
a board has been built and works (`make publish-built TAG=<tag>`).

    make publish          # the real thing: clean tree, HEAD pushed, tag = today
    make publish-draft    # a test: a draft release nobody but the account sees, no tag, no git guards

Needs gh, logged in (gh auth login), and edakit: $EDAKIT, on the PATH, or a clone ../edakit with its .venv.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDAKIT = "edakit"  # resolved in main(), find_edakit()
PUBLISH_DIR = ROOT / "build" / "publish"


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, **kw)


def fail(msg: str) -> None:
    print(f"publish: {msg}", file=sys.stderr)
    sys.exit(1)


def find_edakit() -> str:
    """$EDAKIT, else edakit on the PATH, else the .venv of an edakit clone next to this repository."""
    sibling = ROOT.parent / "edakit" / ".venv" / "bin" / "edakit"
    for cand in (os.environ.get("EDAKIT"), "edakit", str(sibling)):
        if cand and shutil.which(cand):
            return shutil.which(cand)
    fail(f"edakit not found – put it on the PATH, set EDAKIT=/path/to/edakit, or clone edakit to {sibling.parent.parent.parent}")


def projects() -> list[tuple[str, Path]]:
    """(board, edakit.toml) of the root project and every variant, in that order."""
    found = []
    for toml in [ROOT / "edakit.toml", *sorted((ROOT / "variants").glob("*/edakit.toml"))]:
        cfg = tomllib.loads(toml.read_text())
        boards = list(cfg.get("boards", {}))
        if len(boards) != 1:
            fail(f"{toml.relative_to(ROOT)}: expected one board, found {boards}")
        found.append((boards[0], toml))
    return found


def current_release(toml: Path) -> str:
    """The run folder name of the current release, from `edakit release current`."""
    p = run([EDAKIT, "release", "current", "--config", str(toml)])
    m = re.match(r"current release: (\S+) ", p.stdout)
    if p.returncode != 0 or not m:
        fail(f"{toml.relative_to(ROOT)}: no current release\n{p.stdout}{p.stderr}")
    return m.group(1)


def collect(board: str, toml: Path, stage: Path) -> dict:
    cfg = tomllib.loads(toml.read_text())
    reports = toml.parent / cfg["project"].get("reports", "build/release")
    run_name = current_release(toml)
    fab = reports / run_name / "fab"
    order_files = [fab / board / f"{n}_{board}.{e}" for n, e in (("gerber", "zip"), ("bom", "csv"), ("cpl", "csv"))]
    extra = {fab / f"polarity_{board}.png": f"polarity_{board}.png", fab / "manifest.json": f"manifest_{board}.json"}
    for f in [*order_files, *extra]:
        if not f.is_file():
            fail(f"{board}: {f.relative_to(ROOT)} missing")

    p = run([EDAKIT, "release", "verify", "--config", str(toml), *map(str, order_files)])
    print(p.stdout.rstrip())
    if p.returncode != 0:
        fail(f"{board}: edakit release verify refused the files of {run_name} – not published")

    for f in order_files:
        shutil.copy2(f, stage / f.name)
    for f, name in extra.items():
        shutil.copy2(f, stage / name)
    manifest = json.loads((fab / "manifest.json").read_text())
    return {
        "board": board,
        "run": run_name,
        "git": manifest.get("git", "?"),
        "fab_sha256": manifest.get("fab_sha256", "?"),
        "files": [f.name for f in order_files] + list(extra.values()),
    }


def previous_release() -> str | None:
    """Tag of the newest published release (drafts excluded), or None."""
    p = run(["gh", "release", "list", "--exclude-drafts", "--json", "tagName,createdAt", "--limit", "20"])
    if p.returncode != 0:
        fail(f"gh release list failed: {p.stderr}")
    rels = sorted(json.loads(p.stdout), key=lambda r: r["createdAt"], reverse=True)
    return rels[0]["tagName"] if rels else None


def previous_sums(tag: str) -> dict[str, str]:
    """{file name: sha256} of the previous release's SHA256SUMS; empty if it has none."""
    with tempfile.TemporaryDirectory() as tmp:
        p = run(["gh", "release", "download", tag, "--pattern", "SHA256SUMS", "--dir", tmp])
        if p.returncode != 0:
            return {}
        sums = {}
        for line in (Path(tmp) / "SHA256SUMS").read_text().splitlines():
            digest, _, name = line.partition("  ")
            sums[name] = digest
        return sums


def write_sums(stage: Path) -> dict[str, str]:
    sums = {}
    for f in sorted(stage.iterdir()):
        if f.name in ("SHA256SUMS", "notes.md"):
            continue
        sums[f.name] = hashlib.sha256(f.read_bytes()).hexdigest()
    (stage / "SHA256SUMS").write_text("".join(f"{d}  {n}\n" for n, d in sums.items()))
    return sums


def new_decisions(prev_tag: str | None) -> list[str]:
    """Headings of decisions added to docs/decisions.md since the previous release."""
    if not prev_tag:
        return []
    p = run(["git", "diff", f"{prev_tag}..HEAD", "--", "docs/decisions.md"])
    return [line[1:].lstrip("# ").strip() for line in p.stdout.splitlines() if line.startswith("+## D-")]


def repo_url() -> str:
    p = run(["gh", "repo", "view", "--json", "url", "-q", ".url"])
    if p.returncode != 0:
        fail(f"gh repo view failed: {p.stderr}")
    return p.stdout.strip()


def notes(tag: str, head: str, boards: list[dict], sums: dict[str, str], prev_tag: str | None, draft: bool) -> str:
    prev = previous_sums(prev_tag) if prev_tag else {}
    repo = repo_url()
    blob = f"{repo}/blob/{head}"  # links into the state the files were made from; relative links do not work in release notes
    lines = []
    if draft:
        lines += ["**Test of the publishing script – to be deleted.**", ""]
    lines += [
        "Manufacturing files of the Christmas bell's boards at git "
        f"[{head[:7]}]({repo}/commit/{head}): every board passed "
        "edakit's release gate (RELEASED), with the circuit review M-1, the layout review M-5 and the regulatory "
        "review M-6 signed. The boards are built for private use (decision D-16); the regulatory review is support, "
        "not legal advice.",
        "",
        "**Pre-release** until a board of this state has been built and works.",
        "",
        "| Board | Gate run | Manufacturing files (fab hash) | Since the previous release |",
        "|---|---|---|---|",
    ]
    for b in boards:
        order = [f for f in b["files"] if not f.startswith(("polarity_", "manifest_"))]
        if not prev:
            change = "first release"
        elif all(prev.get(f) == sums[f] for f in order):
            change = f"unchanged since {prev_tag}"
        else:
            change = f"changed since {prev_tag}"
        lines.append(f"| {b['board']} | {b['run']} ({b['git']}) | `{b['fab_sha256'][:12]}…` | {change} |")
    decisions = new_decisions(prev_tag)
    if decisions:
        lines += ["", f"Decisions since {prev_tag} ([docs/decisions.md]({blob}/docs/decisions.md)):", ""]
        lines += [f"- {d}" for d in decisions]
    lines += [
        "",
        "**To order at JLCPCB:** per board `gerber_<board>.zip`, with assembly `bom_<board>.csv` and `cpl_<board>.csv`; "
        "`tht` is a bare board. Choose \"Order Number: Specify Position\". `polarity_<board>.png` shows the parts' "
        "positions and polarity for hand soldering. `manifest_<board>.json` is edakit's record of the gate run with "
        "the files' hashes; `SHA256SUMS` covers every file here. Building and using the boards: "
        f"[hardware/README.md]({blob}/hardware/README.md) and [variants/README.md]({blob}/variants/README.md).",
        "",
    ]
    return "\n".join(lines)


def git_guards() -> str:
    """The tree is clean and HEAD is on origin/main. Returns HEAD's SHA."""
    if run(["git", "status", "--porcelain", "--untracked-files=no"]).stdout.strip():
        fail("uncommitted changes – commit first, the tag must name the state the files were made from")
    p = run(["git", "fetch", "origin"])
    if p.returncode != 0:
        fail(f"git fetch failed: {p.stderr}")
    head = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    if run(["git", "merge-base", "--is-ancestor", head, "origin/main"]).returncode != 0:
        fail("HEAD is not on origin/main – push first")
    return head


def free_tag(wanted: str) -> str:
    """`wanted`, or `wanted-2`, `-3`, … if the remote already has that tag."""
    tag, n = wanted, 1
    while run(["git", "ls-remote", "--tags", "origin", f"refs/tags/{tag}"]).stdout.strip():
        n += 1
        tag = f"{wanted}-{n}"
    return tag


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--draft", action="store_true", help="a draft release for a test: no tag, no git guards")
    ap.add_argument("--tag", help="the tag (default: today's date, YYYY-MM-DD)")
    args = ap.parse_args()

    global EDAKIT
    EDAKIT = find_edakit()
    if not shutil.which("gh"):
        fail("gh not found – install the GitHub CLI and log in (gh auth login)")
    if run(["gh", "auth", "status"]).returncode != 0:
        fail("gh is not logged in (gh auth login)")
    head = run(["git", "rev-parse", "HEAD"]).stdout.strip() if args.draft else git_guards()
    tag = args.tag or dt.date.today().isoformat()
    if args.draft:
        tag = f"draft-test-{tag}"
    else:
        tag = free_tag(tag)

    stage = PUBLISH_DIR / tag
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)

    boards = [collect(board, toml, stage) for board, toml in projects()]
    sums = write_sums(stage)
    prev_tag = previous_release()
    (stage / "notes.md").write_text(notes(tag, head, boards, sums, prev_tag, args.draft))

    cmd = ["gh", "release", "create", tag, "--title", f"Manufacturing files {tag}", "--notes-file", str(stage / "notes.md"),
           "--prerelease"]
    if args.draft:
        cmd += ["--draft", "--title", f"DRAFT test {tag}"]
    else:
        cmd += ["--target", head]
    cmd += [str(f) for f in sorted(stage.iterdir()) if f.name != "notes.md"]
    p = run(cmd)
    if p.returncode != 0:
        fail(f"gh release create failed:\n{p.stdout}{p.stderr}")
    url = p.stdout.strip()

    if not args.draft:
        run(["git", "fetch", "--tags", "origin"])
    print()
    print(f"published: {url}")
    print(f"files for the order: {stage}")
    print("  " + ", ".join(f"{b['board']}: {b['run']}" for b in boards))
    if args.draft:
        print(f"this was a test – delete it: gh release delete {tag} --yes")
    else:
        print(f"after a board has been built and works: make publish-built TAG={tag}")


if __name__ == "__main__":
    main()
