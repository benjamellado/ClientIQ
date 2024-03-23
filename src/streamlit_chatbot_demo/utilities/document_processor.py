from docx import Document
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from io import StringIO
import os


class DocumentProcessor:
    def __init__(self, project_name, base_dir="sessions"):
        """
        Initializes the object with the project name and optional base directory.

        Parameters:
            project_name (str): The name of the project.
            base_dir (str): The base directory where project files are stored. Defaults to "sessions".
        """
        self.project_name = project_name
        self.base_dir = base_dir
        self.documents_dir = os.path.join(base_dir, project_name, "documents")
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.docsearch = None  # This will be initialized after indexing

    def _extract_text_docx(self, docx_file):
        """
        Extract text from a DOCX file.

        Args:
            docx_file (str): The path to the DOCX file.

        Returns:
            str: The extracted text from the DOCX file.
        """
        # Load the DOCX file using python-docx
        doc = Document(docx_file)

        # Extract the text from each paragraph in the document
        full_text = [para.text for para in doc.paragraphs]

        # Join the text from each paragraph into a single string, using newline as separator
        return "\n".join(full_text)

    def _extract_text_pdf(self, pdf_file):
        """
        Extract text from a PDF file using pdfminer.six.

        Parameters:
            pdf_file (file-like object): The PDF file to extract text from.

        Returns:
            str: The extracted text from the PDF file.
        """
        # Create a StringIO object to store the extracted text
        output_string = StringIO()

        # Parameters for pdfminer.six layout analysis
        laparams = LAParams()

        # Extract the text from the PDF file and store it in the StringIO object
        extract_text_to_fp(
            pdf_file, output_string, laparams=laparams, output_type="text", codec=None
        )

        # Get the extracted text from the StringIO object
        text = output_string.getvalue()

        # Close the StringIO object
        output_string.close()

        # Return the extracted text
        return text

    def process_documents(self, uploaded_files):
        """
        Process multiple uploaded document files.

        This function takes a list of uploaded files and extracts text from
        each file. It supports DOCX and PDF files. If the file type is not
        supported, it is ignored.

        Args:
            uploaded_files (List[FileUpload]): List of uploaded files.

        Returns:
            List[str]: List of text extracted from the documents.
        """
        # List to store the text extracted from each document
        documents_text = []

        # Loop through each uploaded file
        for uploaded_file in uploaded_files:

            # Check if the file is a DOCX file
            if uploaded_file.name.endswith(".docx"):
                # Extract text from DOCX
                document_text = self._extract_text_docx(uploaded_file)

            # Check if the file is a PDF file
            elif uploaded_file.name.endswith(".pdf"):
                # Extract text from PDF
                document_text = self._extract_text_pdf(uploaded_file)

            # Add additional conditions here for other file types

            # Append the extracted text to the list
            documents_text.append(document_text)

        # Return the list of extracted texts
        return documents_text

    def index_documents(self, documents_text):
        """
        Index the extracted documents using LangChain's FAISS integration.

        Args:
            documents_text (List[str]): List of text extracted from the documents.

        Returns:
            int: Number of indexed documents.
        """
        # Index the extracted documents using LangChain's FAISS integration

        # Use LangChain's FAISS integration to index the documents
        self.docsearch = FAISS.from_texts(documents_text, self.embeddings)

        # If self.docsearch and self.docsearch.index exist, return the number of indexed documents
        # Otherwise, return 0
        return (
            self.docsearch.index.ntotal  # Number of indexed documents
            if self.docsearch
            and self.docsearch.index  # Check if docsearch and index exist
            else 0  # Default to 0 if docsearch or index does not exist
        )
