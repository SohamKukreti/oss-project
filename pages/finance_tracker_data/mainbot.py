import getpass
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import chromadb.api

load_dotenv()

def generateResponse(question, filename = "taxdata"):
    if os.path.exists("pages/finance_tracker_data/taxdata.txt"):
        print("file path exists\n\n\n\n")
    else:
        print("File taxdata.txt does not exist at the specified path ooga booga.")
    llm = ChatOpenAI(model="gpt-4o-mini")

    import bs4
    from langchain import hub
    from langchain_chroma import Chroma
    from langchain_community.document_loaders import WebBaseLoader
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    from langchain_openai import OpenAIEmbeddings
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.document_loaders import CSVLoader
    from langchain_community.document_loaders import TextLoader
    # Load, chunk and index the contents of the blog.
    # loader = CSVLoader(file_path='pages/data/data  - item.csv',
    # csv_args={
    # 'delimiter': ',',
    # 'quotechar': '"',
    # 'fieldnames': ['Index', 'Height', 'Weight']
    # })

    loader = TextLoader(file_path = f"pages/finance_tracker_data/{filename}.txt")

    docs = loader.load()
    print(docs[0].page_content[:100])
    print(docs[0].metadata)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")


    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    response = rag_chain.invoke(question)

    # cleanup
    vectorstore.delete_collection()
    chromadb.api.client.SharedSystemClient.clear_system_cache()
    return response


