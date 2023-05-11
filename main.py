from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

# Replace book.pdf with any pdf of your choice
my_pdf = input("PDF 파일 경로를 입력하세요. 혹은 파일을 끌어다 여기에 놓으세요: ")
loader = UnstructuredPDFLoader(my_pdf)
pages = loader.load_and_split()
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(pages, embeddings).as_retriever()

# Choose any query of your choice
answer = y
while answer != "n":
    question = input("무엇이든 물어보세요: ")
    query = question  
    docs = docsearch.get_relevant_documents(query)
    chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
    output = chain.run(input_documents=docs, question=query)
    print(output)
    proceed = input("더 궁금한 점이 있나요? (y/n): ")
    answer == proceed
print("Cheers~! :)")
