"""Web search tool using DuckDuckGo results."""
try:
    from ddgs import DDGS
except ImportError:  # Fallback for older installs.
    from duckduckgo_search import DDGS


def search(query):
    output = ""
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            output += f"Title: {r['title']}\n"
            output += f"URL: {r['href']}\n"
            output += f"Description: {r['body']}\n\n"
    

    return output.strip()   