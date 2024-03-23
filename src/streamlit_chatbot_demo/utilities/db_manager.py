import pandas as pd
import sqlite3
import os
import streamlit as st


class DBManager:
    def __init__(self, project_name, base_dir="sessions"):
        """
        Initialize the Database Manager.

        Args:
            project_name (str): The name of the project.
            base_dir (str, optional): The base directory. Defaults to "sessions".
        """
        # The name of the project
        self.project_name = project_name
        # The base directory
        self.base_dir = base_dir
        # The path to the SQLite database file
        self.db_path = self._init_db_path()

    def _init_db_path(self):
        """
        Determines and creates the directory for the SQLite database, constructing
        the database file path within the project's directory.
        """
        db_dir = os.path.join(self.base_dir, self.project_name, "database")
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        return os.path.join(db_dir, f"{self.project_name}.db")

    def load_and_insert_data(self, file, table_name):
        """
        Loads data from an uploaded table file (CSV or Excel) into a specific table
        within the SQLite database associated with this project.

        Args:
            file (File): The uploaded file.
            table_name (str): The name of the table to insert the data into.
        """
        # Print the database path to the Streamlit console
        st.write(f"Attempting to connect to database at: {self.db_path}")

        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_path)

        # Determine the file type and read into a pandas DataFrame
        if file.type == "text/csv":
            df = pd.read_csv(file)  # Read CSV file
        else:  # Defaulting to Excel for other file types; extend as needed
            df = pd.read_excel(file)  # Read Excel file

        # Insert the DataFrame into the specified table in the database
        df.to_sql(table_name, conn, if_exists="replace", index=False)

        # Close the database connection
        conn.close()

    def process_files(self, uploaded_files):
        """
        Processes each uploaded table file, extracting the table name from the file name
        and loading its data into the database.

        Args:
            uploaded_files (List[File]): List of uploaded files.

        Returns:
            str: The path to the SQLite database file.
        """
        # Loop through each uploaded file
        for uploaded_file in uploaded_files:
            # Infer table name from the file name (excluding extension)
            # os.path.splitext(filename) returns a tuple with the filename
            # and the extension, so we use [0] to extract just the filename.
            table_name = os.path.splitext(uploaded_file.name)[0]

            # Load and insert the data from the uploaded file into the table
            # with the inferred name.
            self.load_and_insert_data(uploaded_file, table_name)

        # Return the path to the SQLite database file.
        return self.db_path
