"""Alert generation based on log analysis thresholds."""
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class Alert:
    severity: str  # "critical", "warning", "info"
    message: str
    metric: str
    value: float
    threshold: float
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

class AlertEngine:
    def __init__(self, thresholds: Dict):
        self.thresholds = thresholds
        self.alerts: List[Alert] = []

    def check_error_rate(self, error_rate: float):
        threshold = self.thresholds.get("error_rate_threshold", 0.05)
        if error_rate > threshold:
            severity = "critical" if error_rate > threshold * 2 else "warning"
            self.alerts.append(Alert(
                severity=severity,
                message=f"Error rate {error_rate:.2%} exceeds threshold {threshold:.2%}",
                metric="error_rate", value=error_rate, threshold=threshold,
            ))

    def check_all(self, analysis_summary: Dict):
        status = analysis_summary.get("status_codes", {})
        if status:
            self.check_error_rate(status.get("error_rate", 0))

    def get_alerts(self) -> List[Alert]:
        return self.alerts

    def print_alerts(self):
        if not self.alerts:
            print("No alerts triggered.")
            return
        for alert in self.alerts:
            icon = {"critical": "[CRIT]", "warning": "[WARN]", "info": "[INFO]"}.get(alert.severity, "[?]")
            print(f"{icon} {alert.message}")
