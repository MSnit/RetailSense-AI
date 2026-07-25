from customer_module.customer_db import create_customer_folder

from database.database import (
    add_customer,
    generate_next_customer_id
)

from customer_module.capture_images import capture_images
from database.database import add_customer


def register_customer():



    customer_name = input("Enter Customer Name: ").strip()

    if not customer_name:
        print("Customer name cannot be empty.")
        return

    customer_id = generate_next_customer_id()

    print(f"\nCustomer ID: {customer_id}")

    customer_folder = create_customer_folder(customer_id)

    print("\nLook at the camera...")

    image_count = capture_images(customer_folder)

    if image_count == 0:
        print("\nRegistration cancelled.")
        print("No face images were captured.")
        return

    # Save customer to SQLite
    add_customer(
        customer_id,
        customer_name,
        image_count
    )

    

    print("\nRegistration Successful!")
    print(f"Customer ID   : {customer_id}")
    print(f"Customer Name : {customer_name}")
    print(f"Images        : {image_count}")


if __name__ == "__main__":
    register_customer()