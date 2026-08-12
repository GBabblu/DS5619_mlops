import argparse
import csv
import json

import yaml


REQUIRED_KEYS = [
    "input_path",
    "input_format",
    "high_value_threshold",
    "output_path",
]


def load_config(path):
    """Load a YAML config file and validate required keys are present."""

    with open(path, "r") as file:
        data = yaml.safe_load(file)

    if data is None:
        data = {}

    for key in REQUIRED_KEYS:
        if key not in data:
            raise ValueError(f"{key} not present in yaml file")

    return data


def load_transactions(path, fmt):
    """Load transactions from CSV or JSON according to fmt."""

    if fmt not in ("csv", "json"):
        raise ValueError(f"Unsupported input format: {fmt}")

    with open(path, "r") as file:
        if fmt == "csv":
            transactions = list(csv.DictReader(file))
        else:
            transactions = json.load(file)

    if not isinstance(transactions, list):
        raise ValueError("Transaction data must be a list")

    for transaction in transactions:
        if not isinstance(transaction, dict):
            raise ValueError("Each transaction must be a dictionary")

        if "amount" not in transaction:
            raise ValueError("Transaction missing required key: amount")

        if "is_fraud" not in transaction:
            raise ValueError("Transaction missing required key: is_fraud")

    return transactions


def run_pipeline(config):
    """Run the config-driven transaction summary pipeline."""

    rows = load_transactions(
        config["input_path"],
        config["input_format"],
    )

    n = len(rows)

    total_amount = sum(
        float(row["amount"])
        for row in rows
    )

    n_fraud = sum(
        1
        for row in rows
        if (
            isinstance(row["is_fraud"], bool)
            and row["is_fraud"]
        )
        or (
            isinstance(row["is_fraud"], str)
            and row["is_fraud"].strip().lower() == "true"
        )
    )

    n_high_value = sum(
        1
        for row in rows
        if float(row["amount"]) > config["high_value_threshold"]
    )

    report = {
        "n_transactions": n,
        "total_amount": round(total_amount, 2),
        "fraud_rate": round(n_fraud / n, 4) if n else 0.0,
        "n_high_value": n_high_value,
        "high_value_threshold": config["high_value_threshold"],
    }

    with open(config["output_path"], "w") as file:
        json.dump(report, file, indent=2)

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Config-driven fraud transaction summary pipeline"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to a YAML config file",
    )

    args = parser.parse_args()

    config = load_config(args.config)
    report = run_pipeline(config)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
