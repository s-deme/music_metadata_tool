"""Run the test command whenever tracked source files change."""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path


DEFAULT_PATHS = ("src", "tests", "pyproject.toml", "README.md", "config.json")
DEFAULT_COMMAND = ("./bin/test",)
POLL_INTERVAL_SECONDS = 1.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Watch project files and run tests when changes are detected.",
    )
    parser.add_argument(
        "command",
        nargs="*",
        help="Command to run when files change. Defaults to ./bin/test.",
    )
    parser.add_argument(
        "--path",
        action="append",
        dest="paths",
        default=[],
        help="Path to watch. Can be specified multiple times.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=POLL_INTERVAL_SECONDS,
        help="Polling interval in seconds.",
    )
    return parser.parse_args()


def iter_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if not path.exists():
            continue
        if path.is_file():
            files.append(path)
            continue
        files.extend(
            child
            for child in path.rglob("*")
            if child.is_file() and ".git" not in child.parts and "__pycache__" not in child.parts
        )
    return sorted(files)


def snapshot(paths: list[Path]) -> dict[Path, tuple[int, int]]:
    state: dict[Path, tuple[int, int]] = {}
    for file_path in iter_files(paths):
        stat = file_path.stat()
        state[file_path] = (stat.st_mtime_ns, stat.st_size)
    return state


def run_command(command: list[str]) -> int:
    print(f"[watch] running: {' '.join(command)}", flush=True)
    return subprocess.run(command, check=False).returncode


def main() -> int:
    args = parse_args()
    command = args.command or list(DEFAULT_COMMAND)
    watched_paths = [Path(path) for path in (args.paths or list(DEFAULT_PATHS))]
    interval = max(0.2, args.interval)

    previous = snapshot(watched_paths)
    run_command(command)

    print(
        "[watch] watching:",
        ", ".join(str(path) for path in watched_paths),
        flush=True,
    )
    try:
        while True:
            time.sleep(interval)
            current = snapshot(watched_paths)
            if current == previous:
                continue

            changed = sorted(set(current) ^ set(previous) | {path for path in current if current[path] != previous.get(path)})
            print("[watch] change detected:", ", ".join(str(path) for path in changed[:10]), flush=True)
            if len(changed) > 10:
                print(f"[watch] and {len(changed) - 10} more files", flush=True)
            run_command(command)
            previous = current
    except KeyboardInterrupt:
        print("[watch] stopped", flush=True)
        return 130


if __name__ == "__main__":
    sys.exit(main())
