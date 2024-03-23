from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.globals import set_debug

# Enable debugging for detailed logs
set_debug(True)


class ClientIQ:
    def __init__(self, db_path, vectorstore, llm_model="gpt-3.5-turbo", temperature=0):
        """
        Initialize the ClientIQ chatbot with a specified database path, vectorstore,
        language model, and temperature setting for response generation variability.

        Args:
            db_path (str): The path to the database.
            vectorstore (VectorStore): The vectorstore to use for document similarity search.
            llm_model (str, optional): The language model to use. Defaults to "gpt-3.5-turbo".
            temperature (float, optional): The temperature setting for response generation. Defaults to 0.
        """
        # Initialize the document retriever with similarity search settings
        # The vectorstore is used for document similarity search
        self.vectorstore = vectorstore
        self.retriever = vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": 2}
        )

        # Attempt to load the database from the specified path
        print("Attempting to load DB from", db_path)

        # Initialize the SQL agent to interact with the database
        # The llm_model specifies the language model to use, and
        # temperature controls the variability of the generated responses
        self.db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
        self.llm = ChatOpenAI(model=llm_model, temperature=temperature)
        self.agent_executor = create_sql_agent(
            self.llm, db=self.db, agent_type="openai-tools", verbose=True
        )

        # Setup for multi-query retrieval to enrich document context
        # This configuration sets up the multi-query retriever
        self.multiquery_retriever = self.setup_multiquery_retriever()

        # Configure and assemble the retrieval and response generation chain
        # This setup configures the processing chain
        self.setup_chain()

    def setup_multiquery_retriever(self):
        """
        Configures the multi-query retriever to generate alternative queries for
        document retrieval, aiming to cover various perspectives on the business question.
        """
        multiquery_retrieval_prompt = """
        You are an AI language model assistant with a specialization in business intelligence and client management. Your task is to dissect the given user question into five different versions, each focusing on a unique aspect of business understanding or client-specific inquiry. This approach aims to retrieve the most relevant documents from a vector database, overcoming the limitations of distance-based similarity searches by covering various business perspectives and client needs. Consider aspects like financial implications, strategic decisions, client relationship dynamics, and operational efficiency.

        Provide these alternative questions separated by newlines.

        Original question: {question}
        """
        multiquery_prompt_template = PromptTemplate(
            input_variables=["question"], template=multiquery_retrieval_prompt
        )

        return MultiQueryRetriever.from_llm(
            retriever=self.retriever,
            llm=self.llm,
            prompt=multiquery_prompt_template,
        )

    def setup_chain(self):
        """
        Sets up the LangChain processing chain integrating document insights, data insights,
        and the language model to generate comprehensive, reasoned responses to user questions.
        """
        prompt_str = """As a business intelligence AI, your goal is to synthesize information from multiple sources to provide a comprehensive answer to the main question. Consider the implications of the data from both the Document Insights and Data Insights in the context of our client-focused business environment. Analyze the combined data to offer strategic insights, actionable recommendations, and any relevant data points or trends that support your conclusions.

        Ensure your response is concise, data-driven, and directly addresses the business needs related to the question. Avoid generic responses by leveraging the specific information provided.

        Context:
        - Document Insights: {multiquery}
        - Data Insights: {SQLAgent}

        Main Question: {question}

        Answer (please provide a structured and reasoned response based on the context above):
        """

        self.prompt = ChatPromptTemplate.from_template(prompt_str)

        self.retrieval = RunnableParallel(
            {
                "SQLAgent": self.agent_executor,
                "multiquery": self.multiquery_retriever,
                "question": RunnablePassthrough(),
            }
        )

        self.output_parser = StrOutputParser()

        # Assemble the full chain
        self.chain = self.retrieval | self.prompt | self.llm | self.output_parser

    def answer_question(self, question):
        """
        Invokes the processing chain with a given question and returns the generated answer.

        Args:
            question (str): The user's question.

        Returns:
            str: The generated answer.
        """
        # Invoke the processing chain with the given question and return the generated answer.
        # The processing chain consists of document retrieval, data retrieval,
        # language model inference and response parsing.

        return self.chain.invoke(question)
