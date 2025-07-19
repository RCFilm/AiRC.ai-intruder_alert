import re
import time

INPUT_LOG = "/fail2ban_logs/proxy-host-1_access.log"
OUTPUT_LOG = "/normalized/proxy-host-1_access.normalized.log"

LOG_PATTERN = re.compile(r"\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}) [^\]]+\] - (\d{3}) .*?([0-9\.]+|\:\:1)")

def normalize_log():
    with open(INPUT_LOG, "r") as infile, open(OUTPUT_LOG, "a") as outfile:
        for line in infile:
            match = LOG_PATTERN.match(line)
            if match:
                date_time, status, client_ip = match.groups()
                normalized_line = f"[{date_time}] {status} {client_ip}\n"
                outfile.write(normalized_line)
                outfile.flush()

if __name__ == "__main__":
    while True:
        normalize_log()
        time.sleep(5)

