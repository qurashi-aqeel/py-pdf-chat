import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai

from langchain_community.vectorstores.faiss import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Read the text from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# Divide text into chunks for better processing.
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000, chunk_overlap=1000
    )
    chunks = text_splitter.split_text(text)
    return chunks


# Convert text to vector
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"
    )  # type: ignore
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    # Save vectors in local system inside the folder faiss_index
    vector_store.save_local("faiss_index")


def get_conversational_chain():
    prompt_template = "Answer the questions from the context. Make sure to answer the questions which are from the scope properly and correctly.\nContext: {context}?\nQuestion: {question}\n\n Answer:"

    model = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3
    )  # type: ignore

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


# Get user input:
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"
    )  # type: ignore

    new_db = FAISS.load_local(
        "faiss_index", embeddings,
        allow_dangerous_deserialization=True
    )

    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )

    print(response)
    st.write("Bot: ", response["output_text"])


def main():
    st.set_page_config("Chat with PDF's")
    st.header("Leveraging the benifit of Gemini pro")

    user_question = st.text_input("Ask a question from the PDF files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu")
        pdf_doc = st.file_uploader("Upload PDF files")
        if st.button("Submit and process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_doc)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")


if __name__ == "__main__":
    main()
