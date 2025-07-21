import os
import gzip
import re

# Location of the Fail2ban log file inside the container. The docker-compose
# file mounts the host log to this path, so the script can read it directly.
INPUT_LOG = os.environ.get("INPUT_LOG", "/app/backend/data/logs/fail2ban.log")
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
        for line in iter_lines(INPUT_LOG):
            m = LOG_LINE.search(line)
            if m:
                dt, ip = m.groups()
                out.write(f"[{dt}] {ip}\n")


if __name__ == '__main__':
    normalize()
