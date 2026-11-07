from customer_service import handle_customer_message

customer_id = "CUST-1001"

message = (
    "I am contacting support again. "
    "What is happening with my previous payment issue?"
)

print("\nCUSTOMER MESSAGE:")
print(message)

print("\nPROCESSING CUSTOMER REQUEST...\n")

result = handle_customer_message(customer_id, message)

print("RECALLED MEMORIES:")
for memory in result["memories"]:
    print("-", memory)

print("\nAI SUPPORT RESPONSE:")
print(result["response"])