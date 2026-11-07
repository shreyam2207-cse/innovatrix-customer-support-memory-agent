from hindsight_memory import (
    retain_customer_memory,
    recall_customer_memory
)

customer_id = "CUST-1001"

conversation = (
    "The customer reported that ₹1500 was deducted from their bank "
    "account, but the order failed. We checked the transaction. "
    "The issue is still unresolved. The customer wants an update "
    "before attempting another payment."
)

print("\n1. Saving customer interaction...")

message = retain_customer_memory(customer_id, conversation)
print(message)

print("\n2. Recalling customer history...")

memories = recall_customer_memory(
    customer_id,
    "What happened with this customer's previous payment?"
)

if memories:
    for memory in memories:
        print("\nRECALLED MEMORY:")
        print(memory)
else:
    print("No memories returned yet. Try again after a short wait.")