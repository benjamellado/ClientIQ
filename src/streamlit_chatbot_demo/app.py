import streamlit as st
import os
from utilities.db_manager import DBManager
from utilities.document_processor import DocumentProcessor
from chatbot.chatbot import ClientIQ

# Initialize session state variables for chatbot initialization and user question.
st.session_state.setdefault("chatbot_initialized", False)
st.session_state.setdefault("user_question", "")


# Define a function to setup session directories based on the project name.
def setup_session_directory(project_name):
    """
    Setup directories for the current session's database and documents.

    Args:
        project_name (str): Name of the project.

    Returns:
        str: Path to the session directory.
    """
    # Construct the session path by joining 'sessions' and project_name
    session_path = os.path.join("sessions", project_name)

    # Create sub-directories 'database' and 'documents' in the session path
    # if they don't already exist.
    for sub_dir in ["database", "documents"]:
        os.makedirs(os.path.join(session_path, sub_dir), exist_ok=True)

    return session_path


# Main Streamlit UI
st.title("Chatbot Demo")

# Input for the project name and setup session directory upon entry.
project_name = st.text_input("Enter your project name:")
if project_name:
    session_directory = setup_session_directory(project_name)
    st.success(f'Session "{project_name}" initialized.')

# File uploaders for table files and document files.
uploaded_table_files = st.file_uploader(
    "Upload table files (Excel, CSV):", accept_multiple_files=True, key="tables"
)
uploaded_document_files = st.file_uploader(
    "Upload document files (DOCX, PDF, etc.):", accept_multiple_files=True, key="docs"
)

# Button to trigger chatbot initialization after file uploads.
if st.button("Initialize Chatbot") and project_name:
    if uploaded_table_files:
        # Process and load table files into the database.
        db_manager = DBManager(project_name)
        db_manager.process_files(uploaded_table_files)
        st.success("Database has been created and populated with table data.")

    if uploaded_document_files:
        # Process and index document files.
        doc_processor = DocumentProcessor(session_directory)
        documents_text = doc_processor.process_documents(uploaded_document_files)
        num_indexed_docs = doc_processor.index_documents(documents_text)
        st.success(f"Indexed {num_indexed_docs} documents for fast retrieval.")

    # Initialize the ClientIQ chatbot with processed data, if available.
    if uploaded_table_files or uploaded_document_files:
        st.session_state.chatbot = ClientIQ(
            db_path=db_manager.db_path if "db_manager" in locals() else None,
            vectorstore=(
                doc_processor.docsearch if "doc_processor" in locals() else None
            ),
            llm_model="gpt-3.5-turbo-0125",
        )
        st.session_state.chatbot_initialized = True
    else:
        st.error(
            "Please upload at least one table file or document file to initialize the chatbot."
        )

# Interface for asking questions if the chatbot has been initialized.
if st.session_state.chatbot_initialized and "chatbot" in st.session_state:
    st.title("ClientIQ Chatbot")
    question = st.text_input("Ask me anything:", key="question")

    if question:
        answer = st.session_state.chatbot.answer_question(question)
        st.write("Answer:", answer)
