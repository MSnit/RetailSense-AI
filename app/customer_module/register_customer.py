from customer_db import *
from capture_images import capture_images

customers = load_customers()

customer_name = input("Enter Customer Name: ")

customer_id = generate_customer_id(customers)

new_customer = {
    "customer_id": customer_id,
    "name": customer_name,
    "images": 0
}

customers.append(new_customer)


print(f"\nCustomer {customer_name} registered successfully!")
print(f"Customer ID: {customer_id}")

customer_folder = create_customer_folder(customer_id)
image_count = capture_images(customer_folder)
new_customer["images"] = image_count

save_customers(customers)

print(f"Folder Created: {customer_folder}")

print("\nRegistration Successful!")
print(f"Customer ID : {customer_id}")
print(f"Customer Name : {customer_name}")
print(f"Images Captured : {image_count}")

def register_customer():
    # Move all your current registration code here

    if __name__ == "__main__":
        register_customer()