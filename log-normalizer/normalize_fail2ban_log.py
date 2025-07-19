import os
import gzip
import re
from glob import glob

INPUT_DIR = os.environ.get("INPUT_DIR", "/logs")
OUTPUT_FILE = os.environ.get("OUTPUT_FILE", "/normalized/fail2ban.normalized.log")

LOG_LINE = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?(?:Ban|Found) ([0-9a-fA-F:.]+)")


def iter_lines(path):
    if path.endswith('.gz'):
        opener = gzip.open
        mode = 'rt'
    else:
        opener = open
        mode = 'r'
    with opener(path, mode) as f:
        for line in f:
            yield line


def normalize():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w') as out:
        for fname in sorted(glob(os.path.join(INPUT_DIR, 'fail2ban.log*'))):
            for line in iter_lines(fname):
                m = LOG_LINE.search(line)
                if m:
                    dt, ip = m.groups()
                    out.write(f"[{dt}] {ip}\n")


if __name__ == '__main__':
    normalize()
