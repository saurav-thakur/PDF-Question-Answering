Here’s a high-level design (HLD) for the **PDF Question Answering System**:

---

### 1. **Overview**

The PDF Question Answering System is designed to allow users to upload PDF documents and ask questions about the document content via a WebSocket-based real-time chat interface. The backend processes PDFs, splits and stores their content, and responds to user queries using a language model to perform natural language understanding and retrieval.

### 2. **Architecture Components**

1. **Frontend**:

   - **WebSocket Client Interface**: A simple HTML page with JavaScript establishes a WebSocket connection for real-time question and answer exchange.
   - **User Interface**: Allows users to type questions. Displays questions asked and answers received from the backend.

2. **Backend**:

   - **FastAPI Application**: Acts as the main entry point, handling API requests and WebSocket communication.
   - **APIRouter**: Provides routes for PDF uploads, question-answering, and WebSocket communication.
   - **WebSocket Connection**: Facilitates real-time communication between the client and server for Q&A interactions.

3. **Database**:

   - **Relational Database**: Stores metadata about uploaded PDF files in PostgreSQL. Neon Tech is used for production environment.

4. **Document Processing**:

   - **PDF Parsing**: Uses a utility to read and split PDF content into text chunks for easier processing.
   - **Embeddings**: Generates embeddings for PDF content using pre-trained language models for efficient text retrieval.

5. **LLM (Large Language Model) and Retrieval**:

   - **Vector Database**: PineCone Stores text chunk embeddings for semantic similarity retrieval, enabling the system to retrieve relevant chunks from the document.
   - **LLM Model**: Answers user queries based on relevant content retrieved from the document.

6. **Caching and Rate Limiting**:

   - **Rate Limiter** (SlowAPI): Restricts request rates per user to prevent abuse. For now only upload implements rate limiting as SlowAPI does not support WebSocket rate limiting.
   - **Caching**: Optionally caches recent document answers to speed up repeated or similar queries.

7. **Cloud Infrastructure**:
   - **Storage**: Stores PDF files (e.g., on AWS S3 or blob storage).
   - **Deployment**: The FastAPI service and WebSocket server are containerized and deployed, potentially using Docker and managed on cloud services like AWS or GCP.

---

### 3. **Workflow**

1. **PDF Upload**:

   - The user uploads a PDF through an API endpoint (`/api/v1/pdf-qa/upload`).
   - The PDF content is read, parsed, and split into chunks, which are stored in the database and indexed in the vector database.

2. **Question-Answer Interaction**:

   - A WebSocket connection (`/api/v1/pdf-qa/ws`) is established when a user opens the chat interface.
   - The user sends a question via WebSocket.
   - The backend retrieves relevant text chunks based on semantic similarity from the vector database.
   - The LLM generates an answer using retrieved text and returns it through the WebSocket connection.

3. **Rate Limiting and Monitoring**:
   - The backend uses rate limiting to restrict the frequency of requests from individual users.
   - Logging and monitoring tools track API usage, WebSocket connections, and errors for debugging and analytics.

---

### 4. **Deployment and CI/CD**

- Continuous Integration (CI) and Continuous Deployment (CD) is triggered on `development` and `main` branch pushes, which runs tests, checks for code quality, and builds the Docker container. The Docker image is deployed to production, and a cloud provider i.e AWS ECR is used to host and manage containers.

---

### 5. **Component Details**

| Component        | Technology                  | Purpose                                        |
| ---------------- | --------------------------- | ---------------------------------------------- |
| Frontend         | HTML, JavaScript, WebSocket | User interface for question-answering          |
| Backend          | FastAPI, SlowAPI            | Main API, WebSocket, rate-limiting             |
| PDF Parsing      | PyPDFLoader                 | Reads and splits PDF content                   |
| Embeddings       | Hugging Face Transformers   | Generates embeddings for text chunks           |
| Vector Database  | Pinecone                    | Stores and retrieves embeddings for similarity |
| Database         | PostgreSQL                  | Stores metadata and other relevant data        |
| Rate Limiter     | SlowAPI                     | Controls request rates for different endpoints |
| Cloud Storage    | File Storage                | Stores uploaded PDF files                      |
| Containerization | Docker                      | Packages and deploys application               |
| CI/CD            | GitHub Actions              | Automates testing and deployment               |

---

### 6. **Security and Error Handling**

- **Authentication & Authorization**: Implemented for file uploads and WebSocket access if required.
- **Data Validation**: Ensures PDF format and file size limits for uploads.
- **Error Handling**: Logs all errors, particularly during PDF parsing and WebSocket communication.
- **Rate Limiting**: Prevents abuse by restricting request frequency using SlowAPI.
- **Environment-based Configurations**: Manages configurations based on development, testing, and production environments.

---

This HLD provides a structured design for building, deploying, and scaling the PDF Question Answering System with clear separation of responsibilities across components, ensuring efficiency and modularity in the application.
