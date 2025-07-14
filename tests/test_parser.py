"""Tests for log parser."""
import unittest
from src.parser import LogParser

class TestLogParser(unittest.TestCase):
    def test_apache_combined(self):
        parser = LogParser("apache_combined")
        line = '192.168.1.1 - - [01/Jan/2025:00:00:01 +0000] "GET /index.html HTTP/1.1" 200 1234'
        result = parser.parse_line(line)
        self.assertEqual(result["ip"], "192.168.1.1")
        self.assertEqual(result["status"], 200)
        self.assertEqual(result["method"], "GET")

    def test_invalid_line(self):
        parser = LogParser("apache_combined")
        result = parser.parse_line("garbage data")
        self.assertTrue(result.get("parse_error", False))

    def test_json_format(self):
        parser = LogParser("json")
        result = parser.parse_line('{"level": "INFO", "message": "test"}')
        self.assertEqual(result["level"], "INFO")

if __name__ == "__main__":
    unittest.main()
