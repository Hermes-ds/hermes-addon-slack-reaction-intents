from pathlib import Path
import os
import sys


def _maybe_add_hermes_source() -> None:
    """Allow standalone addon tests to import Hermes modules.

    Preferred: set HERMES_AGENT_SRC to a local hermes-agent checkout.
    Fallback: if this addon repo lives under a Hermes workspace scaffold path,
    walk upward and add the first parent containing gateway/ and hermes_cli/.
    """
    explicit = os.getenv("HERMES_AGENT_SRC", "").strip()
    candidates = []
    if explicit:
        candidates.append(Path(explicit).expanduser())

    here = Path(__file__).resolve()
    repo_root = here.parents[1]
    if repo_root.exists():
        sys.path.insert(0, str(repo_root))

    for parent in here.parents:
        if (parent / "gateway").exists() and (parent / "hermes_cli").exists():
            candidates.append(parent)
        if parent.name == ".hermes" and parent.parent.exists():
            candidates.append(parent.parent)

    for candidate in candidates:
        if candidate.exists() and (candidate / "gateway").exists() and (candidate / "hermes_cli").exists():
            sys.path.insert(0, str(candidate))
            return


_maybe_add_hermes_source()
