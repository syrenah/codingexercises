import argparse
import json
import socket
import urllib.request

from ddgs import DDGS
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

load_dotenv()


@tool
def search_remote_ok(
    role: str,
    locations: str = "",
    employment_type: str = "any",
    contract_duration: str = "",
    max_results: int = 20,
) -> str:
    """Search Remote OK for current openings matching role and optional job filters."""
    role = role.strip()
    if not role:
        return "Please provide a role or job title."

    request = urllib.request.Request(
        "https://remoteok.com/api",
        headers={"User-Agent": "Mozilla/5.0 coding-exercises-job-search"},
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            payload = json.load(response)
    except Exception as error:
        return f"Remote OK API request failed: {error}"

    location_terms = [
        location.strip().lower()
        for location in locations.split(",")
        if location.strip()
    ]
    employment_type = employment_type.lower().strip()
    duration = contract_duration.lower().strip()
    matches = []

    for job in payload[1:] if isinstance(payload, list) else []:
        if not isinstance(job, dict):
            continue

        title = str(job.get("position", job.get("title", "")))
        company = str(job.get("company", ""))
        description = str(job.get("description", ""))
        tags = " ".join(str(tag) for tag in job.get("tags", []))
        location = str(job.get("location", "Remote"))
        searchable = " ".join(
            [title, company, description, tags, location]
        ).lower()

        if role.lower() not in searchable:
            continue
        if location_terms and not any(
            location_term in searchable for location_term in location_terms
        ):
            continue
        if employment_type not in ("any", "all", ""):
            if employment_type in ("contract", "contractor", "freelance"):
                if "contract" not in searchable and "contractor" not in searchable:
                    continue
            elif employment_type in ("full-time", "full time", "permanent"):
                if "contract" in searchable and "full-time" not in searchable:
                    continue
        if duration and duration not in searchable:
            continue

        matches.append(
            {
                "title": title,
                "company": company,
                "location": location,
                "url": str(job.get("url", "")),
                "posted": str(job.get("date", "")),
            }
        )
        if len(matches) >= max(1, min(max_results, 50)):
            break

    if not matches:
        return "No matching Remote OK openings were found."

    return json.dumps(matches, indent=2)


@tool
def search_job_sites(
    role: str,
    locations: str = "",
    employment_type: str = "any",
    contract_duration: str = "",
    max_results: int = 10,
) -> str:
    """Search web-indexed job boards for openings and return titles, snippets, and URLs."""
    filters = []
    if locations.strip():
        filters.append(locations.strip())
    if employment_type.strip().lower() not in ("", "any", "all"):
        filters.append(employment_type.strip())
    if contract_duration.strip():
        filters.append(contract_duration.strip())

    query = " ".join([role.strip(), *filters, "job"])
    if not role.strip():
        return "Please provide a role or job title."

    results = DDGS().text(
        f"{query} -site:linkedin.com/jobs",
        max_results=max(1, min(max_results, 20)),
    )
    if not results:
        return "No job openings were found in web search."

    return "\n\n".join(
        f"{result.get('title', '')}\n{result.get('body', '')}\n"
        f"URL: {result.get('href', '')}"
        for result in results
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find job openings from Remote OK and web-indexed job boards."
    )
    parser.add_argument("role", help="Job title or role to search for")
    parser.add_argument(
        "--locations",
        default="",
        help='Comma-separated locations, such as "Remote, Tampa, FL"',
    )
    parser.add_argument(
        "--employment-type",
        choices=("any", "full-time", "contract"),
        default="any",
        help="Desired employment type",
    )
    parser.add_argument(
        "--duration",
        default="",
        help='Contract duration, such as "3 months" or "6 months"',
    )
    parser.add_argument("--max-results", type=int, default=10)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        with socket.create_connection(("localhost", 11434), timeout=2):
            pass
    except OSError as error:
        raise SystemExit(
            "Ollama is not running at http://localhost:11434. Start Ollama "
            "and install the llama3.2 model, then run this agent again."
        ) from error

    model = ChatOllama(model="llama3.2", temperature=0)
    agent = create_agent(
        model=model,
        tools=[search_remote_ok, search_job_sites],
        system_prompt=(
            "You are a job-search assistant. Find current openings that fit the "
            "requested role, locations, employment type, and contract duration. "
            "Call both search tools when appropriate, de-duplicate results by URL, "
            "and rank the strongest matches first. Clearly separate contract duration "
            "when it is stated versus only inferred. Always include source URLs. "
            "Do not claim an opening is verified or eligible when the listing does "
            "not contain that information."
        ),
    )

    question = (
        f"Find job openings for the role: {args.role}. "
        f"Locations: {args.locations or 'Any location'}. "
        f"Employment type: {args.employment_type}. "
        f"Contract duration: {args.duration or 'Not specified'}. "
        f"Return up to {args.max_results} strong matches."
    )
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
