from database.database import add_visit


def log_visit(customer_id):

    try:

        add_visit(customer_id)

        print(f"Visit Logged: {customer_id}")

    except Exception as error:

        print(f"Visit logging failed: {error}")