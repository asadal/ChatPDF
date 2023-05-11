from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import streamlit as st

def app():
    st.set_page_config(page_title=Chat with PDF, page_icon="📄")
    st.image("https://cdn.iconscout.com/icon/free/png-256/free-chat-2130787-1794829.png", width=150)
    st.title("Chat with PDF")
    st.subheader("Upload PDF and chat with it. Enjoy!")
   
    my_pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if my_pdf is not None:
        loader = UnstructuredPDFLoader(my_pdf)
        pages = loader.load_and_split()
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma.from_documents(pages, embeddings).as_retriever()
        answer = y
        while answer != "n":
            question = st.text_input("무엇이든 물어보세요.")
            query = question
            docs = docsearch.get_relevant_documents(query)
            chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
            output = chain.run(input_documents=docs, question=query)
            st.write(output)
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
