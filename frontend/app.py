
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="PDF Research Assistant",
    page_icon="📚",
    layout="wide"
)

# Custom interface styling

st.markdown("""
<style>
/* Main application background */
.stApp {
    background-color: #F6F2E9;
    color: #332D26;
}

header[data-testid="stHeader"] {
    background-color: #F6F2E9;
}

/* Content width */
.block-container {
    max-width: 1100px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* Headings and text */
h1, h2, h3 {
    color: #332D26 !important;
}

p, label, span {
    color: #454238;
}

/* Cards and sections */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #E5E6D8;
    border: 1px solid #C9CCB7;
    border-radius: 16px;
    padding: 12px;
}

/* Text inputs */
.stTextInput input {
    background-color: #FFFFFF;
    color: #332D26;
    border: 1px solid #B9BCA5;
    border-radius: 10px;
}

/* Text areas */
.stTextArea textarea {
    background-color: #FFFFFF;
    color: #332D26;
    border-radius: 10px;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background-color: #7B8061;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 0.55rem 1.4rem;
    font-weight: 600;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #62674C;
    color: #FFFFFF;
    border: none;
}

/* PDF uploader */
.stFileUploader {
    background-color: #E5E6D8;
    border-radius: 12px;
    padding: 10px;
}

/* Dividers */
hr {
    border-color: #C9CCB7;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)



# Session state
if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = None

if "document_id" not in st.session_state:
    st.session_state.document_id = None


# Application heading
st.title("📚 AI-Powered PDF Research Assistant")
st.caption("Your documents, your questions, your answers.")
st.divider()


# Logged-in dashboard
if st.session_state.token:

    st.success(f"Welcome, {st.session_state.username}!")

    # PDF upload section
    with st.container(border=True):

        st.subheader("📄 Upload Your Document")

        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"]
        )

        if st.button("Upload PDF", use_container_width=True):

            if uploaded_file is not None:

                headers = {
                    "Authorization": f"Bearer {st.session_state.token}"
                }

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf"
                    )
                }

                try:
                    response = requests.post(
                        f"{API_URL}/documents/upload",
                        headers=headers,
                        files=files,
                        timeout=180
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.session_state.document_id = data["document_id"]

                        st.success("Your PDF has been processed successfully!")

                        col1, col2 = st.columns(2)

                        with col1:
                            st.metric(
                                "Total Pages",
                                data["total_pages"]
                            )

                        with col2:
                            st.metric(
                                "Total Chunks",
                                data["total_chunks"]
                            )

                    else:
                        st.error(
                            response.json().get(
                                "detail",
                                "PDF upload failed"
                            )
                        )

                except requests.RequestException:
                    st.error("Unable to connect to the backend.")

            else:
                st.warning("Please select a PDF first.")

    # Question and answer section
    if st.session_state.document_id:

        with st.container(border=True):

            st.subheader("💬 Ask Your Document")

            question = st.text_input(
                "What would you like to know?",
                placeholder="For example: Explain the main concepts..."
            )

            if st.button("Ask AI", use_container_width=True):

                if question.strip():

                    headers = {
                        "Authorization": f"Bearer {st.session_state.token}"
                    }

                    payload = {
                        "question": question
                    }

                    try:
                        response = requests.post(
                            f"{API_URL}/documents/"
                            f"{st.session_state.document_id}/ask",
                            headers=headers,
                            json=payload,
                            timeout=180
                        )

                        if response.status_code == 200:

                            data = response.json()

                            st.markdown("### ✨ AI Answer")

                            st.markdown(data["answer"])

                            st.divider()

                            st.markdown("### 📖 Sources")

                            for source in data["sources"]:
                                st.write(
                                    f"📄 Page {source['page_number']}"
                                )

                        else:
                            st.error(
                                response.json().get(
                                    "detail",
                                    "Unable to generate answer"
                                )
                            )

                    except requests.RequestException:
                        st.error("Unable to connect to the backend.")

                else:
                    st.warning("Please enter a question.")

    st.divider()

    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.username = None
        st.session_state.document_id = None
        st.rerun()


# Login and registration
else:

    with st.container(border=True):

        st.subheader("Welcome Back")
        st.caption("Login or create an account to continue.")

        choice = st.radio(
    "Choose an option",
    ["Register", "Login"],
    horizontal=True
)

        # Registration
        if choice == "Register":

            st.markdown("### Create Your Account")

            with st.form("register_form"):

                username = st.text_input("Username")
                email = st.text_input("Email")
                password = st.text_input(
                    "Password",
                    type="password"
                )

                register_button = st.form_submit_button(
                    "Create Account",
                    use_container_width=True
                )

            if register_button:

                payload = {
                    "username": username,
                    "email": email,
                    "password": password
                }

                try:
                    response = requests.post(
                        f"{API_URL}/auth/register",
                        json=payload,
                        timeout=30
                    )

                    if response.status_code == 201:
                        st.success(
                            "Account created successfully! Please log in."
                        )

                    else:
                        st.error(
                            response.json().get(
                                "detail",
                                "Registration failed"
                            )
                        )

                except requests.RequestException:
                    st.error("Unable to connect to the backend.")

        # Login
        else:

            st.markdown("### Login to Your Account")

            with st.form("login_form"):

                email = st.text_input("Email")

                password = st.text_input(
                    "Password",
                    type="password"
                )

                login_button = st.form_submit_button(
                    "Login",
                    use_container_width=True
                )

            if login_button:

                payload = {
                    "email": email,
                    "password": password
                }

                try:
                    response = requests.post(
                        f"{API_URL}/auth/login",
                        json=payload,
                        timeout=30
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.session_state.token = data["access_token"]
                        st.session_state.username = email

                        st.rerun()

                    else:
                        st.error(
                            response.json().get(
                                "detail",
                                "Login failed"
                            )
                        )

                except requests.RequestException:
                    st.error("Unable to connect to the backend.")


st.divider()

st.caption("AI-Powered PDF Research Assistant · Built with FastAPI, RAG and Streamlit")
