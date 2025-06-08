# FinSolve RBAC Chatbot 🤖💼

## Project Overview 📋
**FinSolve Technologies**, a leading FinTech company, was facing significant challenges with communication delays and data silos across its departments (**Finance**, **Marketing**, **HR**, **Engineering**, **C-Level**, and **General Employees**). To address these inefficiencies and improve decision-making, an **Internal Chatbot** with **Role-Based Access Control (RBAC)** has been developed 🚀.

This project implements a **Retrieval Augmented Generation (RAG)** system that ensures each user can access only the information relevant to their specific role 🔒. The chatbot processes **natural language queries**, retrieves pertinent data from designated departmental knowledge bases, and generates accurate, context-rich responses, all while enforcing strict access controls 🛡️.

## Features ✨
- **User Authentication** 🔑: Secure login for various departmental users.
- **Role-Based Access Control (RBAC)** 🔐: Restricts data access based on the user's assigned role.
  - **Finance Team** 💰: Access to financial reports, expenses, reimbursements.
  - **Marketing Team** 📈: Access to campaign data, customer feedback, sales metrics.
  - **HR Team** 👥: Access to employee data, attendance, payroll, performance reviews.
  - **Engineering Department** 🛠️: Access to technical documentation, processes, guidelines.
- **Natural Language Processing (NLP)** 🗣️: Understands and responds to natural language queries.
- **RAG Architecture** 📚:
  - **Data Retrieval** 🔍: Utilizes a **FAISS** vector store to efficiently search and retrieve relevant documents.
  - **Context Augmentation** 📝: Integrates retrieved documents as context for the Large Language Model.
  - **Response Generation** 💬: Employs **gpt-4** to generate insightful answers.
- **Scalable Backend** ⚙️: Built with **FastAPI** for a robust and high-performance API.
- **Interactive UI** 🖥️: A user-friendly chatbot interface powered by **Streamlit**.

## Tech Stack 🛠️
- **Python** 🐍: Core programming language.
- **FastAPI** 🚀: Backend API framework.
- **LangChain** 🔗: For building the RAG pipeline (document loading, splitting, vector store integration, LLM chaining).
- **OPEN API** 🌐: For accessing the **gpt-4** Large Language Model.
- **Embeddings** 🤖: For generating openaiembeddings.
- **FAISS** 📊: Vector store for efficient similarity search.
- **Streamlit** 📱: Frontend for the chatbot user interface.
- **python-dotenv** 🔧: For managing environment variables.

## Folder Structure 📁
```
FinSolve-RBAC-Chatbot/
├── .env                  # Environment variables (e.g., GROQ_API_KEY) 🔑
├── data_loader.py        # Script to load data, create embeddings, and build vector stores 📚
├── main.py               # FastAPI backend application ⚙️
├── requirements.txt      # Python dependencies 📦
├── app.py                # Streamlit frontend application 🖥️
├── data/                 # Raw data files categorized by department 📂
│   ├── engineering/      # 🛠️
│   │   └── engineering_master_doc.md
│   ├── finance/         # 💰
│   │   ├── financial_summary.md
│   │   └── quarterly_financial_report.md
│   ├── general/         # 🙋
│   │   └── employee_handbook.md
│   ├── hr/              # 👥
│   │   └── hr_data.csv
│   └── marketing/       # 📈
│       ├── marketing_report_2024.md
│       ├── marketing_report_q1_2024.md
│       ├── marketing_report_q2_2024.md
│       ├── marketing_report_q3_2024.md
│       └── market_report_q4_2024.md
└── vector_store/         # Generated FAISS vector store indices 📊
    ├── engineering/      # 🛠️
    │   ├── index.faiss
    │   └── index.pkl
    ├── finance/         # 💰
    │   ├── index.faiss
    │   └── index.pkl
    ├── general/         # 🙋
    │   ├── index.faiss
    │   └── index.pkl
    ├── hr/              # 👥
    │   ├── index.faiss
    │   └── index.pkl
    └── marketing/       # 📈
        ├── index.faiss
        └── index.pkl
```

## Setup and Installation ⚙️
Follow these steps to get the **FinSolve RBAC Chatbot** up and running on your local machine.

### 1. Clone the Repository 📥
```bash
git https://github.com/ldotmithu/FinSolve-RBAC-Chatbot.git
cd FinSolve-RBAC-Chatbot
```

### 2. Create a Virtual Environment 🧪
It's highly recommended to use a virtual environment to manage dependencies.
```bash
python conda create -n ai-agents python=3.10 -y 

conda activate ai-agents 
```

### 3. Install Dependencies 📦
Install all required Python packages using `requirements.txt`.
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables 🔧
Create a `.env` file in the root directory of the project (`FinSolve-RBAC-Chatbot/`) and add your **OPENAI API key**:
```
OPENAI_API_KEY="your_openai_api_key_here"

```

### 5. parcial de datos y vector Store 📚
Run the `data_loader.py` script to process your data, create embeddings, and build the **FAISS vector stores** for each department. This step needs to be performed only once or whenever your `data/` files change.
```bash
python data_loader.py
```
This will create the `vector_store` directory with separate `.faiss` and `.pkl` files for each department.

### 6. Start the FastAPI Backend 🚀
Open a new terminal, activate your virtual environment, and start the **FastAPI server**.
```bash
# first activate env
conda activate ai-agents 
# then run 
uvicorn main:app --reload
```
The API will typically run on [http://127.0.0.1:8000](http://127.0.0.1:8000) or [http://localhost:8000](http://localhost:8000).

### 7. Start the Streamlit Frontend 📱
Open another new terminal, activate your virtual environment, and start the **Streamlit application**.
```bash
# first activate env
conda activate ai-agents 
# then run 
streamlit run app.py
```
This will open the chatbot UI in your web browser, usually at [http://localhost:8501](http://localhost:8501).

## Usage 🖱️
- **Login** 🔑: Use the sidebar on the left to log in with the provided user credentials.
  - **Tony** (Engineering): username: `Tony`, password: `password123` 🛠️
  - **Bruce** (Marketing): username: `Bruce`, password: `securepass` 📈
  - **Sam** (Finance): username: `Sam`, password: `financepass` 💰
  - **Peter** (Engineering): username: `Peter`, password: `pete123` 🛠️
  - **Sid** (Marketing): username: `Sid`, password: `sidpass123` 📈
  - **Natasha** (HR): username: `Natasha`, password: `hrpass123` 👥
- **Chat** 💬: Once logged in, type your query into the text input field and press **Enter**.
- **Role-Based Access** 🔐: The chatbot will retrieve and answer questions based on the data accessible to your authenticated role. For example, **Sam** can ask about **quarterly financial reports**, **Tony** or **Peter** can access **technical documentation**, **Bruce** or **Sid** can query **campaign data**, and **Natasha** can access **employee data**.