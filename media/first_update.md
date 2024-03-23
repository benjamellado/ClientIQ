# Project Overview

## Problems

- Companies manage numerous clients, making it hard to keep up with all their information.
- Updates about clients are often known only to key account managers, leaving the rest of the team out of the loop.
- Development teams sometimes work on features that clients do not actually need or want.
- Companies struggle to maintain a consistent language among their members, and AI tools do not always integrate well due to this language barrier.

## Solutions

- Develop an AI assistant that possesses comprehensive information about each client, capable of updating with every client interaction.
- Specifically, utilize a LangChain agent that combines Q&A with SQLAgents to fully integrate client data and allow for complex queries.
- The bot will also learn the company's language to ensure seamless communication.

## Key Features

- **Seamless Integration**: Reducing the need for clients to provide documents and data manually.
- **Full Integration**: The bot will not only provide data insights but also serve as a playbook containing all necessary information, merging reasoning with data-driven decisions.
- **Company Familiarity**: The bot will use business terms and adapt to the company's specific language.

## Progress So Far

- Extracted data from documents using GPT and JSON schema.
- Implemented Q&A using a vector database (FAISS), RAG, and GPT.
- Created a database from these documents.
- Developed a SQLAgent that can autonomously query data.

## Immediate Next Steps

- Adapt this concept for use in Spanish.
- Integrate document retrieval, Q&A, and SQLAgent into a cohesive system.
- Explore connection with a document storage system (e.g., Notion).
- Establish a connection with an existing database.
- Create a business persona that speaks in business terms, specifically tailored for a Latin audience.

## What I need help with

- Finding data to validate the concept.
- Teaching the bot to learn the company's language without needing data for fine-tuning.
- Figuring out implementation details, both in terms of how the bot will be used and how clients can add their data.
- Deliverables.

## Extra Features and Considerations

- Explore the use of RAT (Retrieval Augmented Thought) for more complex reasoning patterns.
- Develop a simpler bot for internal use as a knowledge base, potentially scaling to a full chatbot business with multiple offerings.
- **Privacy Concerns**: Create user roles within the bot to control access to sensitive information.
- **Feedback Loop**: Include a mechanism for users to report issues or suggest improvements, fostering continuous development and user satisfaction.
- **Notification System**: Add a mechanism to notify for certain processes when there is some news about the clients
