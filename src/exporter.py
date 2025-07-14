"""Export analysis results."""
import json
import csv
import os

class ResultExporter:
    def __init__(self, output_dir="output/"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def to_json(self, data, filename="analysis.json"):
        path = os.path.join(self.output_dir, filename)
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def to_csv(self, records, filename="records.csv"):
        if not records:
            return
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)
