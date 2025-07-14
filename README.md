# Log Analytics Pipeline

An automated log parsing and analytics pipeline supporting Apache, Nginx, JSON, and Syslog formats with alerting and visualization.

## Architecture
```
de-log-analytics-pipeline/
├── src/
│   ├── parser.py        # Multi-format log parser (Apache, Nginx, JSON, Syslog)
│   ├── analyzer.py      # Traffic analysis, error rates, top paths/IPs
│   ├── alerting.py      # Threshold-based alert generation
│   └── visualization.py # Status codes, traffic timeline, top paths plots
├── config/config.yaml
├── tests/test_parser.py
└── main.py
```

## Supported Formats
| Format | Example |
|--------|---------|
| Apache Combined | Standard Apache access logs |
| Nginx | Nginx access logs |
| JSON | Structured JSON logs |
| Syslog | System log format |

## Installation
```bash
git clone https://github.com/mouachiqab/de-log-analytics-pipeline.git
cd de-log-analytics-pipeline
pip install -r requirements.txt
```

## Usage
```bash
python main.py --input data/access.log --format apache_combined
```

## Technologies
- Python 3.9+, pandas, regex, loguru, matplotlib








