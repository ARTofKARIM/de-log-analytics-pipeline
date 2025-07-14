"""Log analysis and statistics computation."""
import pandas as pd
import numpy as np
from collections import Counter
from typing import Dict, List

class LogAnalyzer:
    def __init__(self):
        self.df = None

    def load_records(self, records: List[Dict]):
        self.df = pd.DataFrame(records)
        print(f"Loaded {len(self.df)} log records")
        return self

    def status_code_distribution(self) -> Dict:
        if "status" not in self.df.columns:
            return {}
        dist = self.df["status"].value_counts().to_dict()
        total = len(self.df)
        return {
            "distribution": dist,
            "error_rate": sum(v for k, v in dist.items() if k >= 400) / total,
            "success_rate": sum(v for k, v in dist.items() if 200 <= k < 300) / total,
        }

    def top_paths(self, n=10) -> List:
        if "path" not in self.df.columns:
            return []
        return self.df["path"].value_counts().head(n).to_dict()

    def top_ips(self, n=10) -> List:
        if "ip" not in self.df.columns:
            return []
        return self.df["ip"].value_counts().head(n).to_dict()

    def method_distribution(self) -> Dict:
        if "method" not in self.df.columns:
            return {}
        return self.df["method"].value_counts().to_dict()

    def traffic_over_time(self, time_col="timestamp", freq="1H"):
        if time_col not in self.df.columns:
            return pd.Series(dtype=int)
        ts = pd.to_datetime(self.df[time_col], format="mixed", errors="coerce")
        return ts.dt.floor(freq).value_counts().sort_index()

    def error_analysis(self) -> Dict:
        if "status" not in self.df.columns:
            return {}
        errors = self.df[self.df["status"] >= 400]
        return {
            "total_errors": len(errors),
            "4xx_count": len(errors[errors["status"] < 500]),
            "5xx_count": len(errors[errors["status"] >= 500]),
            "top_error_paths": errors["path"].value_counts().head(5).to_dict() if "path" in errors.columns else {},
        }

    def summary(self) -> Dict:
        return {
            "total_records": len(self.df),
            "parse_errors": int(self.df.get("parse_error", pd.Series()).sum()) if "parse_error" in self.df.columns else 0,
            "status_codes": self.status_code_distribution(),
            "methods": self.method_distribution(),
            "errors": self.error_analysis(),
        }
