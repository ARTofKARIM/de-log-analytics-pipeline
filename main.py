"""Main entry point for log analytics pipeline."""
import argparse
import yaml
from src.parser import LogParser
from src.analyzer import LogAnalyzer
from src.alerting import AlertEngine
from src.visualization import LogVisualizer

def main():
    parser = argparse.ArgumentParser(description="Log Analytics Pipeline")
    parser.add_argument("--input", required=True, help="Log file path")
    parser.add_argument("--format", default="apache_combined", choices=["apache_combined", "json", "syslog", "nginx"])
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    log_parser = LogParser(args.format)
    records = list(log_parser.parse_file(args.input))
    analyzer = LogAnalyzer()
    analyzer.load_records(records)
    summary = analyzer.summary()
    print(f"\nTotal records: {summary['total_records']}")
    print(f"Parse errors: {summary['parse_errors']}")
    print(f"Error rate: {summary['status_codes'].get('error_rate', 0):.2%}")

    alert_engine = AlertEngine(config.get("alerting", {}))
    alert_engine.check_all(summary)
    alert_engine.print_alerts()

    viz = LogVisualizer()
    status_dist = summary["status_codes"].get("distribution", {})
    if status_dist:
        viz.plot_status_distribution(status_dist)
    top_paths = analyzer.top_paths()
    if top_paths:
        viz.plot_top_paths(top_paths)
    print("Analysis complete.")

if __name__ == "__main__":
    main()
