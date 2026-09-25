"""Custom checks for the brain (scaffolded by `henxels init --template brainpick-brain`)."""

import datetime
import re

import yaml

from henxels import statement

_SECTION = re.compile(r"^##\s+(.+?)\s*$")
_DAY = re.compile(r"^(\d{4})-(\d{2})-(\d{2})\.md$")
_CHECKBOX = re.compile(r"^\s*[-*+]\s+\[([ xX])\]\s+(.*?)\s*$")
_DONE = re.compile(r"\(done:\s*(\d{4}-\d{2}-\d{2})\)\s*$")


def _folder(param):
    return str(param).strip().removeprefix("./").strip("/")


def _frontmatter(text):
    """The leading ``---`` YAML block as a dict (empty when absent or unparseable)."""
    if not text or not text.startswith("---"):
        return {}
    lines = text.splitlines()
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


@statement("log_headings_are_dates", help="log.md sections are '## YYYY-MM-DD' headings, newest first")
def log_headings_are_dates(file, scope):
    dates, problems = [], []
    for line in (scope.read_text(file) or "").splitlines():
        m = _SECTION.match(line)
        if not m:
            continue
        try:
            dates.append(datetime.date.fromisoformat(m.group(1)))
        except ValueError:
            problems.append(f"section '{m.group(1)}' — head log sections with an ISO date: ## YYYY-MM-DD")
    if dates != sorted(dates, reverse=True):
        problems.append("order the date sections newest first")
    return problems


@statement("skill_tools_exist", help="every path a skill lists under `tools:` exists, relative to the bundle root")
def skill_tools_exist(param, file, scope):
    """brainpick indexes and points at a skill's tools (spec/85); a path that lands
    nowhere is a broken promise. `param` is the bundle root (./_brain)."""
    root = _folder(param)
    tools = _frontmatter(scope.read_text(file)).get("tools") or []
    if not isinstance(tools, list):
        return f"{file} — `tools:` must be a list of bundle-relative paths"
    missing = [t for t in tools if not scope.exists(f"{root}/{str(t).lstrip('/')}")]
    return [f"{file} — tool {t} does not exist under {root}/ (add it or drop it from `tools:`)" for t in missing]


@statement("archived_journals_sit_under_year_month",
           help="archived journal days live at archive/YYYY/MM/YYYY-MM-DD.md, the folders matching the name")
def archived_journals_sit_under_year_month(param, file, scope):
    """`param` is the archive folder (./_brain/journals/archive)."""
    archive = _folder(param)
    rel = file[len(archive) + 1:] if file.startswith(archive + "/") else file
    name = rel.rsplit("/", 1)[-1]
    m = _DAY.match(name)
    if not m:
        return f"{file} — name an archived day YYYY-MM-DD.md"
    want = f"{m.group(1)}/{m.group(2)}/{name}"
    if rel != want:
        return f"{file} — move it to {archive}/{want} (the day roll keeps archive/YYYY/MM/)"
    return None


@statement("done_todos_are_archived",
           help="a [x] item in open.md carries (done: YYYY-MM-DD) and leaves for archive/YYYY-MM-DD.md the next day; "
                "the archive is day files holding only done items")
def done_todos_are_archived(param, file, scope):
    """`param` is the todo folder (./_brain/todo)."""
    todo = _folder(param)
    rel = file[len(todo) + 1:] if file.startswith(todo + "/") else file
    problems = []
    items = [(m.group(1).lower() == "x", m.group(2)) for m in map(_CHECKBOX.match, (scope.read_text(file) or "").splitlines()) if m]
    if rel == "open.md":
        today = datetime.date.today()
        for done, text in items:
            if not done:
                continue
            m = _DONE.search(text)
            if not m:
                problems.append(f"{file} — '{text[:40]}' is ticked but undated: end it with (done: YYYY-MM-DD)")
                continue
            day = m.group(1)
            if datetime.date.fromisoformat(day) < today:
                problems.append(f"{file} — '{text[:40]}' was done {day}: move the line to {todo}/archive/{day}.md")
        return problems
    if rel.startswith("archive/"):
        name = rel.rsplit("/", 1)[-1]
        if "/" in rel[len("archive/"):] or not _DAY.match(name):
            return f"{file} — an archived to-do file is {todo}/archive/YYYY-MM-DD.md, the day its items were closed"
        for done, text in items:
            if not done:
                problems.append(f"{file} — '{text[:40]}' is still open: it belongs in {todo}/open.md, not the archive")
        return problems
    return None
