"""Log file parser with multiple format support."""
import re
import json
from typing import List, Dict, Generator
from datetime import datetime

class LogParser:
    def __init__(self, log_format="apache_combined", custom_pattern=None):
        self.log_format = log_format
        self.patterns = {
            "apache_combined": r'(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d+) (?P<size>\S+)',
            "syslog": r'(?P<timestamp>\w+ \d+ \S+) (?P<host>\S+) (?P<process>\S+): (?P<message>.*)',
            "nginx": r'(?P<ip>\S+) - \S+ \[(?P<timestamp>[^\]]+)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\d+) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"',
        }
        if custom_pattern:
            self.patterns["custom"] = custom_pattern
            self.log_format = "custom"

    def parse_line(self, line: str) -> Dict:
        line = line.strip()
        if not line:
            return {}
        if self.log_format == "json":
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                return {"raw": line, "parse_error": True}
        pattern = self.patterns.get(self.log_format)
        if not pattern:
            return {"raw": line}
        match = re.match(pattern, line)
        if match:
            parsed = match.groupdict()
            if "status" in parsed:
                parsed["status"] = int(parsed["status"])
            if "size" in parsed and parsed["size"] != "-":
                try:
                    parsed["size"] = int(parsed["size"])
                except ValueError:
                    parsed["size"] = 0
            return parsed
        return {"raw": line, "parse_error": True}

    def parse_file(self, filepath: str) -> Generator[Dict, None, None]:
        with open(filepath, "r", errors="replace") as f:
            for line_num, line in enumerate(f, 1):
                parsed = self.parse_line(line)
                if parsed:
                    parsed["_line_num"] = line_num
                    yield parsed

    def parse_batch(self, filepath: str, batch_size: int = 10000) -> Generator[List[Dict], None, None]:
        batch = []
        for record in self.parse_file(filepath):
            batch.append(record)
            if len(batch) >= batch_size:
                yield batch
                batch = []
        if batch:
            yield batch
