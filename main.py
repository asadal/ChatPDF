from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import streamlit as st
import chardet

def decode_pdf(pdf_file):
    # Detect the encoding of the PDF file
    encoding = chardet.detect(pdf_file.read())['encoding']
    
    # If the encoding is None, use UTF-8
    if encoding is None:
        encoding = 'utf-8'
    # Decode the PDF file
    pdf_file_string = pdf_file.read().decode(encoding)

    return pdf_file_string

def app():
    st.set_page_config(page_title="Chat with PDF", page_icon="🗒️")
    st.image("https://cdn.iconscout.com/icon/free/png-256/free-chat-2130787-1794829.png", width=150)
    st.title("Chat with PDF")
    st.subheader("Upload PDF and chat with it. Enjoy!")

    # Get the OpenAI API key from the environment
    openai_api_key = st.secrets['openai']["OPENAI_API_KEY"]

    # If the OpenAI API key is not set, raise an error
    if openai_api_key is None:
        st.error("Did not find openai_api_key, please set it as an environment variable.")

    # Upload a PDF file
    my_pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if my_pdf is not None:
        # Load the PDF file
        pdf_file_string = decode_pdf(my_pdf)
        loader = UnstructuredPDFLoader(pdf_file_string)
        pages = loader.load_and_split(filename=my_pdf.name)

        # Create an OpenAI embedding model
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

        # Create a Chroma document searcher
        docsearch = Chroma.from_documents(pages, embeddings).as_retriever()

        # Start a chat loop
        answer = "y"
        while answer == "y":
            # Get the user's question
            question = st.text_input("무엇이든 물어보세요.")
            query = question

            # Get the relevant documents from the document searcher
            docs = docsearch.get_relevant_documents(query)

            # Create a question-answering chain
            chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")

            # Run the question-answering chain
            output = chain.run(input_documents=docs, question=query)

            # Write the output to the chat
            st.write(output)

            # Ask the user if they have any more questions
            proceed = st.text_input("더 궁금한 점이 있나요?")
            if st.button("예, 물어볼게요."):
                answer = 'y'
            elif st.button("안, 물어볼게요."):
                answer = 'n'
            else:
                pass
        st.write("Cheers~! :-)")
        st.end()

if __name__ == "__main__":
    app()
