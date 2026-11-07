from ai_agent import generate_support_response

customer_message = (
    "I contacted support yesterday because "
    "₹1500 was deducted but my order failed. "
    "Can you help me?"
)

memories = [
    "Customer reported that ₹1500 was deducted "
    "but the order failed.",

    "The issue was unresolved. The customer "
    "wanted an update before attempting another payment."
]

print("Testing Groq AI...\n")

answer = generate_support_response(
    customer_message,
    memories
)

print("AI SUPPORT RESPONSE:\n")
print(answer)