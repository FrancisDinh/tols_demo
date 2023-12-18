import random
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

def create_rag_chain():
    llm = OpenAI(model_name="gpt-3.5-turbo",temperature=0.7,max_tokens=100)
    rag_chain = load_qa_chain(llm, chain_type='stuff')
    return rag_chain

def answer_idk():
    answers = [
        "I'm sorry, but I don't have that information.",
        "Unfortunately, I don't have the answer you're looking for.",
        "I'm not familiar with that topic, so I can't provide any insight.",
        "I'm afraid I don't know the answer to your question."
    ]
    return random.choice(answers)

# improve prompt like assignment 1
def get_answer_from_chain(chain, knowledge_base, question):
    doc = knowledge_base.search_from_knowledge_base(question)
    print(f"Doc: {doc} \n")
    if doc is None:
        return answer_idk()
    return chain.run(input_documents=doc,question=question)