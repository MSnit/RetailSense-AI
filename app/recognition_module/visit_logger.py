import json
import os
from datetime import datetime

LOG_FILE = "datasets/visit_logs.json"


def log_visit(customer_id):

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)
    else:
        logs = []

    logs.append({
        "customer_id": customer_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)

    print(f"Visit Logged: {customer_id}")