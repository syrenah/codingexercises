from dotenv import load_dotenv
import socket

from ddgs import DDGS
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

load_dotenv()


@tool
def web_search(query: str) -> str:
    """Search the web and return titles, snippets, and source URLs."""
    results = DDGS().text(query, max_results=5)
    if not results:
        return "No web results found."

    return "\n\n".join(
        f"{result['title']}\n{result['body']}\nURL: {result['href']}"
        for result in results
    )


@tool
def mercari_search(query: str) -> str:
    """Search web-indexed Mercari listings for an item and return result links."""
    results = DDGS().text(f"site:mercari.com {query}", max_results=5)
    if not results:
        return "No Mercari results found in web search."

    return "\n\n".join(
        f"{result['title']}\n{result['body']}\nURL: {result['href']}"
        for result in results
    )


def main():
    try:
        with socket.create_connection(("localhost", 11434), timeout=2):
            pass
    except OSError as error:
        raise SystemExit(
            "Ollama is not running at http://localhost:11434. Start the Ollama app "
            "and try again."
        ) from error

    model = ChatOllama(model="llama3.2", temperature=0)
    agent = create_agent(
        model=model,
        tools=[web_search, mercari_search],
        system_prompt=(
            "You are a helpful assistant. Use mercari_search for requests to find "
            "products on Mercari. Use web_search for other questions needing "
            "current information. Include source URLs in your answer, and explain "
            "that Mercari search results may not include every active listing."
        ),
    )

    question = input("What would you like to search for? ").strip()
    if not question:
        raise SystemExit("Please enter a question to search for.")

    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
