import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

def get_pdf_text(pdf_docs):
    """Extracts text from a list of uploaded PDF files."""

    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)

        for page in pdf_reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

    return text


def get_text_chunks(text):
    """Splits the extracted text into mangeable chunks."""

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)

    return chunks


def get_vector_store(text_chunks):
    """Generates embeddings and creates a FAISS vector store."""

    if not text_chunks:
        st.warning("No text extracted from PDF's. Cannot create vector store.")
        return

    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")
        st.success("Processing Complete. FAISS index created.")

    except Exception as e:
        st.error(f"Error creating vector store: {e}")
        st.stop()

    return vector_store


def get_conversational_chain():
    """Creates the modern LCEL (Langchain Expression Language) QA chain."""

    prompt_template = """
    Answer the questions as detailed as possible from the provided context. Make sure to provide all the details. If the answer is not in the provided context just say, "Answer is not available in the context" don't provide wrong answer
    
    Context: \n {context} \n
    Question: \n {question} \n
    
    Answer: 
    """
    model = ChatOpenAI(temperature=0.3)

    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": RunnableLambda(lambda x: format_docs(x["input_documents"])),
            "question": lambda x: x["question"],
        }
        | prompt
        | model
        | StrOutputParser()
    )

    return chain


def user_input(user_question):
    """Handles user input, retrives the relevant documents, and get's an answer"""

    try:
        embeddings = OpenAIEmbeddings()

        new_db = FAISS.load_local(
            "faiss_index", embeddings, allow_dangerous_deserialization=True
        )

        docs = new_db.similarity_search(user_question)
        chain = get_conversational_chain()
        response = chain.invoke({"input_documents": docs, "question": user_question})
        print(response)
        st.write("Reply: ", response)

    except FileNotFoundError:
        st.error("FAISS index not found. Please upload and process your PDF's first")

    except Exception as e:
        st.error(f"An error occured: {e}")


def main():
    st.set_page_config(page_title="Chat with PDF", page_icon="🤷‍♂️")

    st.header("Chat with PDF using OpenAI 🤷‍♂️")

    if not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY not found in .env file. Please add it.")
        st.stop()

    user_question = st.text_input("Ask a Question from the PDF file.")

    if user_question:
        if not os.path.exists("faiss_index"):
            st.warning("Please upload and process your PDF files first.")

        else:
            user_input(user_question)

    with st.sidebar:

        st.title("Menu: ")
        pdf_docs = st.file_uploader(
            "Upload your PDF file and click on the submit & process button",
            accept_multiple_files=True,
        )

        if st.button("Submit & Process"):

            if pdf_docs:

                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)

                    if raw_text:
                        text_chunks = get_text_chunks(raw_text)
                        get_vector_store(text_chunks)

                    else:
                        st.warning(
                            "No text could be extracted from the uploaded PDF's."
                        )
            else:
                st.warning("PLease upload at least one PDF file.")


if __name__ == "__main__":
    main()
