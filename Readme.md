# **Project Wiki: Prefect LLM Integration with PostgreSQL**

This wiki provides an overview of the folder structure, tools, libraries, and a step-by-step guide on how to set up and run the project. Additionally, it explains the functionality of each file at a high level.

To visualize full implementation, step into h_events_persistence folder.

 [Youtube Video Walkthrough Playlist](https://www.youtube.com/watch?v=4Lnzn4lw9ig&list=PLteHam9e1FecJQ0jcQKDUAaU20fGQmQ9u)

---

## **Folder Structure**

```
h_events_persistence/
│
├── docker-compose.yml        # Docker Compose file for setting up PostgreSQL and Adminer
├── requirements.txt          # Python dependencies for the project
├── create_table.py           # Script to create the PostgreSQL database table
├── models.py                 # SQLAlchemy model and database connection setup
├── hooks.py                  # Prefect hooks for handling flow completion and failure
├── llm_flow.py               # Prefect flow to query LLM and store results
└── README.md                 # Instructions on how to set up and run the project
```

---

## **Tools and Libraries Used**

### **1. Prefect v3**
- **Prefect** is a workflow orchestration tool that manages data pipelines.
- **Why we use it**: It orchestrates flows, retries, and error handling. Version 3.0.4 is used for managing tasks and flows, and integration with PostgreSQL.

### **2. OpenAI**
- **OpenAI**'s API is used to interact with the LLM (Ollama) model. 
- **Why we use it**: To send questions to an LLM and retrieve responses that we log and store.

### **3. SQLAlchemy**
- **SQLAlchemy** is a Python SQL toolkit and Object Relational Mapper (ORM).
- **Why we use it**: It simplifies the creation and interaction with PostgreSQL databases, enabling us to define models and handle database queries.

### **4. Psycopg2-binary**
- **Psycopg2-binary** is a PostgreSQL adapter for Python.
- **Why we use it**: It enables Python to connect and interact with the PostgreSQL database where flow results are stored.

### **5. Docker Compose**
- **Docker Compose** is a tool used for defining and running multi-container Docker applications.
- **Why we use it**: To set up PostgreSQL and Adminer services for database management in a containerized environment.

---

## **Setup Guide**

### **1. Install Dependencies**

First, create a virtual environment or activate an existing one, then install all dependencies using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

**`requirements.txt`**:
```
prefect
OpenAI
sqlalchemy 
psycopg2-binary
prefect-email
```

### **2. Set Up PostgreSQL and Adminer**

Use Docker Compose to set up the PostgreSQL and Adminer services for database management.

```bash
docker-compose up -d
```

This will spin up PostgreSQL on port `5432` and Adminer on port `8080`. You can access Adminer at [http://localhost:8080](http://localhost:8080) to manage the database.

### **3. Create the PostgreSQL Database Table**

Run the `create_table.py` script to create the table in PostgreSQL for storing the flow results.

```bash
python create_table.py
```

### **4. Run the Prefect Flow**

Run the `llm_flow.py` script to start the Prefect flow, which queries the LLM model and stores the result in PostgreSQL.

```bash
python llm_flow.py
```

### **5. View Results in Adminer**

You can use Adminer to connect to your PostgreSQL database and view the flow results stored in the `flow_results` table.

---

## **Functional Explanation of Each File**

### 1. **`docker-compose.yml`**
- **Purpose**: Sets up two services—PostgreSQL for storing the flow results and Adminer for managing the database.
- **How it works**: It defines the PostgreSQL database with user credentials, creates a volume for persistent storage, and exposes the necessary ports for interaction.

### 2. **`requirements.txt`**
- **Purpose**: Lists all dependencies required for running the project.
- **How it works**: When you run `pip install -r requirements.txt`, all listed libraries, including Prefect, OpenAI, SQLAlchemy, and psycopg2, are installed.

### 3. **`create_table.py`**
- **Purpose**: Creates the `flow_results` table in PostgreSQL.
- **How it works**: It uses SQLAlchemy to define the database schema and creates the table when executed.

### 4. **`models.py`**
- **Purpose**: Defines the schema of the `flow_results` table and establishes the database connection.
- **How it works**: SQLAlchemy is used to map the `FlowResult` class to the `flow_results` table in PostgreSQL. It also defines the connection string to connect to the database.

### 5. **`hooks.py`**
- **Purpose**: Contains hooks that are triggered when a flow is completed or fails.
- **How it works**: The hooks extract the flow result and store it in PostgreSQL by interacting with the `FlowResult` model in `models.py`.

### 6. **`llm_flow.py`**
- **Purpose**: Defines the Prefect flow that sends queries to the LLM and stores the result.
- **How it works**: This file contains a flow with a task that queries the LLM (Ollama), and the result is stored in PostgreSQL using the hooks defined in `hooks.py`.

---

## **Project Workflow Overview**

### High-Level Workflow:
1. **Flow Execution**: A flow (defined in `llm_flow.py`) queries the LLM with a user-defined question.
2. **Flow Result**: The LLM returns a response that is processed and logged.
3. **Result Storage**: Hooks trigger on completion or failure of the flow and store the response (or error message) in the `flow_results` table in PostgreSQL.
4. **Result Management**: The results can be viewed and managed using Adminer.