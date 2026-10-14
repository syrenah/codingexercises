from dotenv import load_dotenv
import socket
load_dotenv()  # Load environment variables from .env file
# ChatPromptTemplate is imported from langchain_core.prompts; it formats chat messages
# and is itself a Runnable (a component with a standard input/output interface).
from langchain_core.prompts import ChatPromptTemplate
# ChatOllama is imported from langchain_ollama; it adapts an Ollama chat model as a Runnable.
from langchain_ollama import ChatOllama

def main():
    model = ChatOllama(model="llama3.2", temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("human", "Explain {topic} in three bullet points."),
    ])
    # LCEL (LangChain Expression Language) uses `|` to compose Runnables in order.
    # This creates a RunnableSequence (the chain): format the prompt, then call the model.
    chain = prompt | model

    # ChatOllama's default local server listens on port 11434.
    try:
        with socket.create_connection(("localhost", 11434), timeout=2):
            pass
    except OSError as error:
        raise SystemExit(
            "Ollama is not running at http://localhost:11434. Install Ollama, "
            "then run `ollama run llama3.2` and try again."
        ) from error

    # Runnable.invoke runs one input through the chain; this dict fills {topic}.
    # The result is a chat message (AIMessage), whose text is available as .content.
    response = chain.invoke({"topic": "LangChain"})
    print(response.content)
    response = chain.invoke({"topic": "butter"})
    print(response.content)
    print("Response: ", end="", flush=True)
    for chunk in chain.stream({"topic": "sailor moon"}):
        print(chunk.content, end="", flush=True)
    print()
if __name__ == "__main__":
    main()