import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATABASE_PATH = os.path.join(BASE_DIR, "datasets", "customers.json")


def load_customers():

    if not os.path.exists(DATABASE_PATH):
        return []

    with open(DATABASE_PATH, "r") as file:
        return json.load(file)


def save_customers(customers):


    with open(DATABASE_PATH, "w") as file:
        json.dump(customers, file, indent=4)

def generate_customer_id(customers):

    if len(customers) == 0:
        return "RS-001"

    last_customer = customers[-1]["customer_id"]

    number = int(last_customer.split("-")[1])

    number += 1

    return f"RS-{number:03d}"

def save_customers(customers):
    with open(DATABASE_PATH, "w") as file:
        json.dump(customers, file, indent=4)

def generate_customer_id(customers):

    if len(customers) == 0:
        return "RS-001"

    last_customer = customers[-1]["customer_id"]

    number = int(last_customer.split("-")[1])

    number += 1

    return f"RS-{number:03d}"

def create_customer_folder(customer_id):

    customer_folder = os.path.join(BASE_DIR, "datasets", "customers", customer_id)

    os.makedirs(customer_folder, exist_ok=True)

    return customer_folder

def get_customer_name(customer_id):

    customers = load_customers()

    for customer in customers:
        if customer["customer_id"] == customer_id:
            return customer["name"]

    return "Unknown"