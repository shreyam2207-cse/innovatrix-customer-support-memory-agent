
import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")

HINDSIGHT_BASE_URL = os.getenv(
    "HINDSIGHT_BASE_URL",
    "https://api.hindsight.vectorize.io"
)

HINDSIGHT_BANK_ID = os.getenv("HINDSIGHT_BANK_ID")


def get_hindsight_client():

    if not HINDSIGHT_API_KEY:
        raise ValueError("Hindsight API key is missing.")

    return Hindsight(
        base_url=HINDSIGHT_BASE_URL,
        api_key=HINDSIGHT_API_KEY
    )


def get_customer_bank_id(customer_id):

    if not customer_id or not customer_id.strip():
        raise ValueError("Customer ID is required.")

    safe_id = customer_id.strip().lower()
    safe_id = safe_id.replace(" ", "-")

    return f"innovatrix-{safe_id}"


def ensure_customer_bank(client, customer_id):

    bank_id = get_customer_bank_id(customer_id)

    try:
        client.create_bank(
            bank_id=bank_id,
            name=f"Innovatrix Support - {customer_id}"
        )

    except Exception as error:
        raise RuntimeError(
            f"Could not create or access customer bank: {error}"
        )

    return bank_id


def retain_customer_memory(customer_id, conversation):

    client = get_hindsight_client()

    try:
        bank_id = ensure_customer_bank(
            client,
            customer_id
        )

        content = (
            f"Customer ID: {customer_id}\n"
            f"Customer-reported information: {conversation}\n"
            "These are customer-provided statements, "
            "not independently verified transaction records."
        )

        client.retain(
            bank_id=bank_id,
            content=content,
            context="Customer support conversation"
        )

        return (
            f"Customer interaction successfully stored "
            f"in {bank_id}."
        )

    finally:
        client.close()


def recall_customer_memory(customer_id, question):

    client = get_hindsight_client()

    try:
        # Create or confirm the customer's memory bank first.
        bank_id = ensure_customer_bank(
            client,
            customer_id
        )

        # Now recall memories from that customer's bank.
        result = client.recall(
            bank_id=bank_id,
            query=question
        )

        return [
            memory.text
            for memory in result.results
        ]

    finally:
        client.close()
