
from hindsight_memory import get_hindsight_client

def customer_bank_id(customer_id):
    safe_id = customer_id.strip().lower()
    safe_id = safe_id.replace(" ", "-")
    return f"innovatrix-{safe_id}"


client = get_hindsight_client()

try:
    # Create one separate memory bank for each customer
    for customer_id in ["CUST-1001", "CUST-2001"]:

        bank_id = customer_bank_id(customer_id)

        client.create_bank(
            bank_id=bank_id,
            name=f"Innovatrix Support - {customer_id}"
        )

        print(f"Created or confirmed bank: {bank_id}")

    # Store a different test message in each bank
    client.retain(
        bank_id=customer_bank_id("CUST-1001"),
        content="CUST-1001 reported that ₹1500 was deducted for a failed order."
    )

    client.retain(
        bank_id=customer_bank_id("CUST-2001"),
        content="CUST-2001 reported that ₹2000 was charged for a failed order."
    )

    # Recall each customer's own memory
    for customer_id in ["CUST-1001", "CUST-2001"]:

        bank_id = customer_bank_id(customer_id)

        print(f"\nMemories for {customer_id}:")

        result = client.recall(
            bank_id=bank_id,
            query="What payment problem did this customer report?"
        )

        for memory in result.results:
            print("-", memory.text)

finally:
    client.close()
