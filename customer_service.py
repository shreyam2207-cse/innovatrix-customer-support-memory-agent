
from hindsight_memory import (
    retain_customer_memory,
    recall_customer_memory
)

from ai_agent import generate_support_response


def handle_customer_message(customer_id, message):

    if not customer_id or not customer_id.strip():
        raise ValueError("Customer ID is required.")

    if not message or not message.strip():
        raise ValueError("Customer message is required.")

    # 1. Recall memories only from this customer's bank
    memories = recall_customer_memory(
        customer_id,
        "Previous customer-reported payment issues, "
        "failed orders, refund concerns and preferences"
    )

    # 2. Generate a response using the customer's history
    answer = generate_support_response(
        customer_message=message,
        memories=memories
    )

    # 3. Store only the customer's own message.
    # AI-generated responses are not stored as customer facts.
    customer_memory = (
        f"Customer ID: {customer_id}\n"
        f"Customer-reported information: {message}\n"
        "These are customer-provided statements, "
        "not independently verified transaction records."
    )

    retain_customer_memory(
        customer_id,
        customer_memory
    )

    return {
        "response": answer,
        "memories": memories
    }
