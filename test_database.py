from app.customer_module.customer_db import *

customers = load_customers()

new_customer_id = generate_customer_id(customers)

print("Next Customer ID:", new_customer_id)