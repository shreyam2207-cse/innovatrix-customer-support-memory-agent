
import html
import re
import streamlit as st

from customer_service import handle_customer_message


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Innovatrix | AI Customer Support",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background-color: #f1f5f9;
    font-family: 'Inter', sans-serif;
}

/* Main page spacing */

.block-container {
    padding-top: 3.5rem;
    padding-bottom: 2rem;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stSidebar"] * {
    color: #f9fafb;
}

.brand {
    font-size: 29px;
    font-weight: 800;
    color: white;
}

.brand span {
    color: #60a5fa;
}

/* Main headings */

.main-heading {
    font-size: 32px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 5px;
}

.main-subtitle {
    color: #475569;
    font-size: 14px;
    margin-bottom: 22px;
}

.chat-heading {
    color: #0f172a;
    font-size: 23px;
    font-weight: 800;
    margin-top: 18px;
}

.chat-description {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 15px;
}

/* Dashboard cards */

.status-card {
    background: white;
    border: 1px solid #dbe3ee;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 18px;
}

.status-label {
    color: #64748b;
    font-size: 12px;
    font-weight: 700;
}

.status-value {
    color: #0f172a;
    font-size: 19px;
    font-weight: 800;
    margin-top: 7px;
}

/* Conversation panel */

[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #d5dfeb !important;
    border-radius: 12px !important;
    background-color: #eaf0f7;
}

/* Message bubbles */

.message-bubble {
    padding: 14px 17px;
    border-radius: 15px;
    font-size: 14px;
    line-height: 1.75;
    overflow-wrap: anywhere;
    color: #172033;
}

.message-bubble strong {
    font-weight: 800;
    color: #0f172a;
}

.message-bubble code {
    background-color: #e2e8f0;
    padding: 2px 5px;
    border-radius: 4px;
    font-size: 13px;
}

/* Customer message */

.user-bubble {
    background-color: #dbeafe;
    border: 1px solid #93c5fd;
    border-bottom-right-radius: 4px;
}

/* AI response */

.assistant-bubble {
    background-color: #ffffff;
    border: 1px solid #dbe3ee;
    border-bottom-left-radius: 4px;
    box-shadow: 0 2px 5px rgba(15, 23, 42, 0.05);
}

/* Message labels */

.message-label {
    display: block;
    font-size: 11px;
    font-weight: 800;
    margin-bottom: 6px;
    letter-spacing: 0.3px;
}

.user-label {
    color: #1d4ed8;
}

.assistant-label {
    color: #2563eb;
}

/* Chat input */

[data-testid="stChatInput"] {
    background-color: white;
    border: 1px solid #cbd5e1;
    border-radius: 14px;
}

/* Buttons */

.stButton button {
    border-radius: 9px;
    font-weight: 600;
}

/* Footer */

.footer {
    color: #64748b;
    font-size: 11px;
    text-align: center;
    padding: 25px 0;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# MESSAGE FORMATTING
# ==========================================

def format_message(content):

    text = str(content)

    # Convert escaped Markdown symbols into normal Markdown.
    text = text.replace(r"\*\*", "**")
    text = text.replace(r"\*", "*")
    text = text.replace(r"\.", ".")

    # Escape HTML to keep customer messages safe.
    safe_text = html.escape(text)

    # Render Markdown bold formatting.
    safe_text = re.sub(
        r"\*\*(.+?)\*\*",
        r"<strong>\1</strong>",
        safe_text,
        flags=re.DOTALL
    )

    # Render inline code formatting.
    safe_text = re.sub(
        r"`([^`]+)`",
        r"<code>\1</code>",
        safe_text
    )

    # Preserve line breaks.
    safe_text = safe_text.replace("\n", "<br>")

    return safe_text


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "memories" not in st.session_state:
    st.session_state.memories = []

if "active_customer" not in st.session_state:
    st.session_state.active_customer = "CUST-1001"

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown(
        '<div class="brand">INNOVA<span>TRIX</span></div>',
        unsafe_allow_html=True
    )

    st.caption("INTELLIGENT CUSTOMER SUPPORT")

    st.divider()

    st.markdown("### Customer Profile")

    customer_id = st.text_input(
        "Customer ID",
        value=st.session_state.active_customer,
        key="customer_input"
    ).strip()

    if customer_id != st.session_state.active_customer:

        st.session_state.messages = []
        st.session_state.memories = []
        st.session_state.pending_prompt = None
        st.session_state.active_customer = customer_id

    st.caption(
        "Each customer has a separate Hindsight memory bank."
    )

    st.divider()

    st.markdown("### 🧠 Customer Memory")

    st.caption("Information recalled from Hindsight")

    if st.session_state.memories:

        for index, memory in enumerate(
            st.session_state.memories,
            start=1
        ):

            with st.expander(f"Memory {index}"):
                st.write(memory)

    else:

        st.info("No recalled memories displayed yet.")

    st.divider()

    if st.button("Clear Chat History", use_container_width=True):

        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

    st.caption(
        "Clearing chat does not delete persistent memory."
    )

    st.divider()

    st.caption("POWERED BY HINDSIGHT + GROQ")


# ==========================================
# MAIN DASHBOARD
# ==========================================

st.markdown(
    '<div class="main-heading">Customer Support Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'Personalized customer support with persistent AI memory.'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# STATUS CARDS
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("""
    <div class="status-card">
        <div class="status-label">AI ASSISTANT</div>
        <div class="status-value">Innovatrix AI</div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="status-card">
        <div class="status-label">ACTIVE CUSTOMER</div>
        <div class="status-value">{html.escape(customer_id or "Not selected")}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="status-card">
        <div class="status-label">MEMORY ENGINE</div>
        <div class="status-value">Hindsight</div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# CONVERSATION HEADING
# ==========================================

st.markdown(
    '<div class="chat-heading">💬 Conversation</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="chat-description">'
    'Customer messages and AI responses appear below.'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# RECEIVE CUSTOMER INPUT FIRST
# ==========================================

prompt = st.chat_input("Type your message here...")

if prompt:

    if not customer_id:

        st.error("Please enter a valid Customer ID.")

    else:

        # Save the submitted message BEFORE rendering
        # the conversation panel.

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        st.session_state.pending_prompt = prompt


# ==========================================
# CONVERSATION PANEL
# ==========================================

with st.container(border=True):

    if not st.session_state.messages:

        # This block appears only when there are no messages.

        st.markdown(
            """
            <div style="
                text-align:center;
                padding:35px 10px;
                color:#64748b;
            ">
                <div style="font-size:32px;">💬</div>
                <div style="font-size:16px;font-weight:700;">
                    Start a conversation
                </div>
                <div style="font-size:13px;margin-top:7px;">
                    Your AI assistant is ready to help.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        # Display all messages in the conversation.

        for message in st.session_state.messages:

            formatted_content = format_message(
                message["content"]
            )

            if message["role"] == "user":

                left, right = st.columns([1, 4])

                with right:

                    st.markdown(
                        f'<div class="message-bubble user-bubble">'
                        f'<span class="message-label user-label">'
                        f'YOU</span>'
                        f'{formatted_content}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

            else:

                left, right = st.columns([4, 1])

                with left:

                    st.markdown(
                        f'<div class="message-bubble assistant-bubble">'
                        f'<span class="message-label assistant-label">'
                        f'INNOVATRIX AI</span>'
                        f'{formatted_content}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

            # Gap between messages.

            st.markdown(
                "<div style='height: 20px;'></div>",
                unsafe_allow_html=True
            )

    # Bottom spacing inside the conversation panel.

    st.markdown(
        "<div style='height: 18px;'></div>",
        unsafe_allow_html=True
    )


# ==========================================
# GENERATE AI RESPONSE
# ==========================================

if st.session_state.pending_prompt is not None:

    current_prompt = st.session_state.pending_prompt

    with st.spinner("Innovatrix AI is thinking..."):

        try:

            result = handle_customer_message(
                customer_id,
                current_prompt
            )

            answer = result["response"]

            st.session_state.memories = result["memories"]

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as error:

            print(f"Application error: {error}")

            st.session_state.messages.append({
                "role": "assistant",
                "content": (
                    "I'm sorry, but I couldn't process your request. "
                    "Please try again."
                )
            })

        finally:

            st.session_state.pending_prompt = None

    # Refresh to display the AI response.

    st.rerun()


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer">
    INNOVATRIX | AI CUSTOMER SUPPORT | POWERED BY HINDSIGHT
</div>
""", unsafe_allow_html=True)
