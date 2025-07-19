"""Simple nginx access log normalizer.

This script watches an nginx access log and writes a simplified line for each
request that matches ``LOG_PATTERN``. The input log is tailed so that only new
lines are processed which prevents duplicates in the output.
"""

from __future__ import annotations

import os
import re
import time
from typing import Generator, Optional


INPUT_LOG = "fail2ban_logs/proxy-host-1_access.log"
OUTPUT_LOG = "normalized/proxy-host-1_access.normalized.log"

# Matches the timestamp, status code and client IP address from a standard
# nginx access log line. IPv4 and simple IPv6 formats are supported.
LOG_PATTERN = re.compile(
    r"\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}) [^\]]+\] \S+ \S+ (\d{3}) \S+\s+(?:\"[^\"]*\"\s+){2}([0-9.:]+)"
)


def _follow(fp) -> Generator[str, None, None]:
    """Generator that yields new lines from ``fp`` as they are written."""

    fp.seek(0, os.SEEK_END)
    while True:
        line = fp.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line


def _normalize_line(line: str) -> Optional[str]:
    """Return a normalized log line or ``None`` if it doesn't match."""

    match = LOG_PATTERN.search(line)
    if not match:
        return None

    date_time, status, client_ip = match.groups()
    return f"[{date_time}] {status} {client_ip}\n"


def normalize_log() -> None:
    os.makedirs(os.path.dirname(OUTPUT_LOG), exist_ok=True)

    with open(INPUT_LOG, "r") as infile, open(OUTPUT_LOG, "a", buffering=1) as outfile:
        for line in _follow(infile):
            normalized = _normalize_line(line)
            if normalized:
                outfile.write(normalized)


def main() -> None:
    """Entry point for running as a script."""

    try:
        normalize_log()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

