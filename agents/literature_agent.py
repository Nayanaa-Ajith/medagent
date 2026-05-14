import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA
from langchain_classic.prompts import PromptTemplate

load_dotenv()

def retrieve_literature(conditions: list, symptoms: list) -> dict:
    # Load vectorstore
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    prompt = PromptTemplate(
        template="""You are a medical literature expert. Based on the following medical documents, provide evidence-based information about the given conditions.

Context from medical literature:
{context}

Conditions to research: {question}

Provide:
1. Evidence-based description of these conditions
2. Recommended diagnostic tests
3. Treatment guidelines from literature
4. Prevention measures

Be specific and cite what the documents say.""",
        input_variables=["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

    query = f"Information about {', '.join(conditions)} with symptoms {', '.join(symptoms)}"
    result = chain.invoke({"query": query})

    # Extract source chunks for explainability
    sources = []
    for doc in result["source_documents"]:
        sources.append({
            "content": doc.page_content[:200],
            "relevance": "high"
        })

    output = {
        "literature_summary": result["result"],
        "sources": sources,
        "num_sources": len(sources)
    }

    print("📚 Literature Retrieval Complete!")
    print(f"   Found {len(sources)} relevant sources")
    return output

if __name__ == "__main__":
    result = retrieve_literature(
        conditions=["meningitis", "encephalitis"],
        symptoms=["severe headache", "high fever", "stiff neck"]
    )
    print("\nLiterature Summary:")
    print(result["literature_summary"])