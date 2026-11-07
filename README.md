# Innovatrix – Customer Support Memory Agent

An AI-powered customer support assistant that remembers previous customer interactions and communication preferences using **Hindsight by Vectorize** and **Groq AI**.

## 1. Problem Statement

Traditional customer support systems often require customers to explain the same problem repeatedly when they contact support again.

This creates frustration, wastes time and makes customer support less personalized.

## 2. Our Solution

Innovatrix is an AI-powered customer support prototype designed to provide continuity across separate customer interactions.

It uses Hindsight as its persistent memory system to retain and recall customer-reported information. Groq AI uses relevant memories to generate personalized responses.

Customers can return to a conversation and ask about previously reported issues without having to explain everything again.

## 3. Key Features

- **Persistent Memory:** Remembers relevant customer information across separate interactions and application restarts.
- **Customer-Specific Memory:** Uses separate Hindsight memory banks for different customer IDs.
- **Personalized Responses:** Uses Groq AI to generate responses based on relevant customer history.
- **Preference Recall:** Remembers communication preferences such as email and SMS.
- **Payment Issue Assistance:** Supports conversations about failed orders, reported deductions and refund concerns.
- **Memory Transparency:** Displays relevant recalled memories in the application.
- **Responsible Responses:** Clearly communicates limitations and does not claim to verify transactions or process refunds.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | User interface |
| Hindsight by Vectorize | Persistent memory |
| Groq AI | AI response generation |
| Python-dotenv | Environment variable management |

## 5. System Architecture

1. Customer enters their customer ID and message.
2. The application retrieves relevant memories from that customer's Hindsight memory bank.
3. Retrieved memories and the current message are passed to Groq AI.
4. Groq generates a personalized response.
5. The customer's new message is stored in Hindsight.
6. During future interactions, the application recalls relevant information.

## 6. Project Structure

```text
Innovatrix/
│
├── app.py
├── ai_agent.py
├── hindsight_memory.py
├── customer_service.py
├── config.py
│
├── test_customer_banks.py
├── test_customer_service.py
├── test_groq.py
├── test_hindsight.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── .env                 # Local credentials; not uploaded
```

## 7. Installation and Setup

### Prerequisites

- Python 3.10 or later
- A Groq API key
- A Hindsight Cloud API key
- Internet connection

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a `.env` file in the project root directory.

Add your own credentials:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b

HINDSIGHT_API_KEY=your_hindsight_api_key
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
HINDSIGHT_BANK_ID=innovatrix-customer-support
```

**Important:** Never share or upload your `.env` file or API keys.

### Step 5: Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 8. Memory Demonstration

Example customer interactions:

**Customer CUST-1001**
- Reported ₹1,500 deducted for a failed order.
- Reported the issue on 6 November 2026.
- Preferred communication method: Email.

**Customer CUST-2001**
- Reported ₹2,000 charged for a failed order.
- Reported the issue on 6 November 2026.
- Preferred communication method: SMS.

When these customers return, Innovatrix can recall their respective information from their separate Hindsight memory banks.

## 9. Responsible AI and Limitations

Innovatrix is a prototype customer support assistant.

It does not:
- Access actual banking or payment gateway systems.
- Verify transactions or refund status.
- Initiate or approve refunds.
- Send emails, SMS messages or notifications.
- Guarantee that a merchant or bank will resolve an issue.

The application treats customer statements as reported information, not independently verified transaction records.

Separate memory banks provide logical customer separation in this prototype. Production deployment would require authentication, authorization, stronger access controls and additional security measures.

## 10. Future Enhancements

- Secure customer authentication and authorization.
- Integration with verified order and payment systems.
- Real email and SMS notification services.
- Advanced memory management and retrieval.
- Analytics for identifying recurring customer issues.
- Production-grade monitoring and security.

## 11. Project Team

**Team:** Innovatrix

**Project:** Customer Support Memory Agent

**Core Focus:** AI Agents, Persistent Memory and Personalized Customer Support

---

*Built using Python, Groq AI and Hindsight by Vectorize.*