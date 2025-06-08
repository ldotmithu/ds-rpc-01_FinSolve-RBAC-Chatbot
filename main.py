import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Dict 

from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI 

load_dotenv()

USERS_DB: Dict[str, Dict[str, str]] = {
    "Tony": {"password": "password123", "role": "engineering"},
    "Bruce": {"password": "securepass", "role": "marketing"},
    "Sam": {"password": "financepass", "role": "finance"},
    "Peter": {"password": "pete123", "role": "engineering"},
    "Sid": {"password": "sidpass123", "role": "marketing"},
    "Natasha": {"password": "hrpass123", "role": "hr"}
}


ROLE_PERMISSIONS = {
    "finance": ["finance"],
    "marketing": ["marketing"],
    "hr": ["hr"],
    "engineering": ["engineering"],
    "employee": ["general"]
}


security = HTTPBasic()
app = FastAPI()

class Query(BaseModel):
    message: str
    role: str

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    user = USERS_DB.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"username": username, "role": user["role"]}

@app.get("/login")
def login(user=Depends(authenticate)):
    return {"message": f"Welcome {user['username']}!", "role": user["role"]}


@app.post("/chat") 
def chat_with_docs(query_data: Query, user=Depends(authenticate)): 
    user_actual_role = user['role']
    target_department_role = query_data.role.lower() 

    if target_department_role not in ROLE_PERMISSIONS.get(user_actual_role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized: {user_actual_role.capitalize()} users cannot access {target_department_role.capitalize()} data."
        )

    vector_store_path = os.path.join("vector_store", target_department_role)

    if not os.path.exists(vector_store_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Knowledge base not found for department: {target_department_role.capitalize()}."
        )

    try:
        db = FAISS.load_local(
            folder_path=vector_store_path,
            embeddings=OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY")),
            allow_dangerous_deserialization=True 
        )
        retriever = db.as_retriever()
        docs = retriever.invoke(query_data.message)
        if not docs:
            return {"response": "I couldn't find relevant information in the knowledge base for your query."}
        prompt = ChatPromptTemplate.from_template(
            "Answer the question using only the context below.\n\n{context}\n\nQuestion: {input}"
        )
        llm = ChatOpenAI(model="gpt-4", api_key=os.getenv("OPENAI_API_KEY"), temperature=0.5)

        chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
        response = chain.invoke({"input": query_data.message, "context": docs})
        return {"response": response}

    except Exception as e:
        import traceback
        print(f"An error occurred in /chat endpoint: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")

@app.get("/")
def root():
    return {"message": "FinSolve RBAC Chatbot API is running."}

@app.get("/test")
def test_authentication(user=Depends(authenticate)):
    return {"message": f"Hello {user['username']}! Your role is {user['role']}.", "role": user["role"]}