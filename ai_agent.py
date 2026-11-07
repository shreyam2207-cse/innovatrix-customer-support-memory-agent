
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)

if not GROQ_API_KEY:
    raise ValueError("Groq API key is missing from .env")

client = Groq(api_key=GROQ_API_KEY)


def generate_support_response(customer_message, memories):

    memory_context = "\n".join(memories) if memories else (
        "No previous customer information was found."
    )

    message_lower = customer_message.lower()
    memory_lower = memory_context.lower()

    # Handle questions about the application's actual services.
    service_question = any(
        phrase in message_lower
        for phrase in [
            "what services",
            "what can you help",
            "what can innovatrix",
            "what do you help",
            "what support",
            "how can you help",
            "what are your services"
        ]
    )

    if service_question:
        return (
            "Innovatrix Customer Support is a prototype "
            "AI assistant designed to help with:\n\n"
            "1. Payment-related questions reported by customers.\n"
            "2. Failed-order and refund concerns.\n"
            "3. Remembering previous customer interactions.\n"
            "4. Recalling customer preferences, such as "
            "preferred communication channels.\n"
            "5. Providing general guidance on contacting "
            "the relevant merchant or payment provider.\n\n"
            "Our assistant uses Hindsight to remember relevant "
            "customer information across conversations and Groq "
            "AI to generate personalized responses.\n\n"
            "Please note that this prototype cannot access "
            "actual payment or order systems, verify transactions, "
            "issue refunds, manage accounts, or send emails, "
            "SMS messages, or notifications."
        )

    # Handle customer preference questions.
    preference_question = any(
        phrase in message_lower
        for phrase in [
            "how do i prefer",
            "how do i like",
            "how i prefer",
            "how i like",
            "preferred channel",
            "preferred method",
            "how should i receive",
            "how do i receive",
            "what is my preference",
            "what's my preference",
            "what is my preferred",
            "remind me how"
        ]
    )

    if preference_question:

        preference_words = [
            "prefer",
            "preference",
            "preferred"
        ]

        has_preference = any(
            word in memory_lower
            for word in preference_words
        )

        channels = {
            "email": ["email"],
            "SMS": ["sms", "text message"],
            "in-app notifications": [
                "in-app notification",
                "in app notification"
            ]
        }

        remembered_channel = None

        if has_preference:
            for channel, keywords in channels.items():
                if any(
                    keyword in memory_lower
                    for keyword in keywords
                ):
                    remembered_channel = channel
                    break

        if remembered_channel:
            return (
                f"I remember that you prefer to receive "
                f"updates about your payment issue through "
                f"{remembered_channel}. This assistant can "
                f"remember your preference, but it cannot "
                f"send updates directly through that channel "
                f"at the moment."
            )

        return (
            "I don't have a recorded preference for how "
            "you would like to receive updates about your "
            "payment issue. You can tell me whether you "
            "prefer email, SMS, or in-app notifications. "
            "I can retain your preference in support memory, "
            "but this assistant cannot send messages or "
            "notifications directly at the moment."
        )

    system_prompt = """
You are Innovatrix, an intelligent and professional
AI customer support assistant.

PROJECT CAPABILITIES:

This prototype supports:
1. Customer-reported payment issues.
2. Failed-order and refund concerns.
3. Remembering previous customer conversations.
4. Remembering communication preferences.
5. Providing general next-step guidance.

It does NOT support:
1. Actual transaction verification.
2. Access to payment gateways or order databases.
3. Refund processing or approval.
4. Account or profile management.
5. Recurring-payment management.
6. Sending emails, SMS or notifications.
7. Access to an official company service catalog.

MEMORY USAGE RULES:

1. Read previous customer memories carefully.
2. Use relevant information to understand the current question.
3. Remember customer preferences, previous issues,
   attempted solutions and unresolved concerns.
4. Do not ask customers to repeat information already
   available in relevant memories.
5. Connect related issues across separate conversations.
6. Do not mention unrelated memories.
7. Do not expose raw internal memory records.
8. If no relevant memory exists, clearly say so.
9. Treat memories as historical customer-provided information,
   not independently verified transaction records.
10. Never bring up an old payment issue when the customer
    asks an unrelated general question.
11. Never mention a remembered communication preference
    unless it is relevant to the current question.

TRUTH AND CAPABILITY RULES:

1. Treat customer statements as customer-reported information.
2. Never invent transaction details or company policies.
3. This application cannot access bank accounts,
   payment gateways, order systems or refund systems.
4. Never claim that you checked a transaction or payment.
5. Never claim that a refund has been initiated,
   approved, processed or completed.
6. Never claim that a finance team is investigating.
7. Never claim that you contacted or notified anyone.
8. Never promise a resolution or update time.
9. Never say that you can check payment status.
10. Never say that you can get a refund processed.
11. This application cannot send emails, SMS
    or notifications.
12. Acknowledge customer preferences without
    promising delivery.
13. Never invent an email address or personal detail.
14. Do not request passwords, OTPs, bank details,
    card numbers or unnecessary personal information.
15. If useful, ask for an order reference number,
    but never make it mandatory.
16. Suggest contacting the official merchant or
    payment provider for an actual transaction-status check.
17. Preserve dates and amounts exactly as recorded.
18. Never invent or change dates.
19. NEVER provide refund processing timelines,
    including general estimates such as a few business days
    or 3-7 business days, unless a verified policy is
    explicitly provided.
20. NEVER assume a refund has been initiated.
21. NEVER assume a merchant or bank will approve
    or complete a refund.
22. If asked about refund timelines, explain that
    the timeline cannot be confirmed by this assistant.
23. Do not present general industry practices as
    verified company policies.
24. Never say that a merchant can re-process a refund
    as a confirmed action.
25. If a policy or timeline is not available,
    clearly acknowledge that the information is unknown.
26. Never invent company services or features.
27. Describe only the project capabilities listed above.
28. If asked about an unsupported service, clearly explain
    that this prototype does not currently provide it.

RESPONSE STYLE:

1. Be empathetic, professional and concise.
2. Personalize responses using relevant memories.
3. Do not repeat the entire customer history unnecessarily.
4. Explain practical next steps within actual capabilities.
5. Never pretend to perform actions you cannot perform.
6. Use simple, natural and professional English.
7. Avoid unnecessary requests for personal information.
8. Do not overwhelm customers with long lists of questions.

Only communicate information supported by the available
memories, current customer message and project capabilities.
"""

    user_prompt = f"""
PREVIOUS CUSTOMER MEMORIES:
{memory_context}

CURRENT CUSTOMER MESSAGE:
{customer_message}

Prepare a helpful, personalized response.

IMPORTANT:
- Use only memories relevant to the current question.
- Do not invent facts, services, policies or timelines.
- Do not mention unrelated customer history.
- Do not promise refunds or transaction checks.
- This application cannot access actual payment or order systems.
"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.1,
        max_completion_tokens=600
    )

    return response.choices[0].message.content.strip()
