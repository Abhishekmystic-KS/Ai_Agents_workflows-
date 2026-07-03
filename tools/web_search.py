# Mock Web Search Tool

# Deterministic knowledge base for testing and evaluations
KNOWLEDGE_BASE = {
    "capital of France": "The capital of France is Paris. It is known for art, fashion, gastronomy, and culture.",
    "founder of Google": "Google was founded in September 1998 by Larry Page and Sergey Brin while they were Ph.D. students at Stanford University.",
    "latest iPhone model in 2026": "In late 2025, Apple released the iPhone 17 series, featuring improved cameras, thinner design, and enhanced AI integration via Apple Intelligence.",
    "current weather in Tokyo": "The current weather in Tokyo is 22°C (71.6°F) and Rainy, with 80% humidity and wind speed of 15 km/h.",
    "weather in London": "The weather in London is 15°C (59°F), Overcast with light drizzle.",
    "population of Tokyo": "Tokyo is the most populous metropolitan area in the world, with a population of approximately 37.4 million people in its greater area."
}

def web_search(query: str) -> str:
    """
    Search the web for up-to-date information on a topic.
    
    Args:
        query: The search query to look up.
        
    Returns:
        A string containing search results.
    """
    print(f"[Tool Execution] web_search called with query: '{query}'")
    
    # Normalize the query to look for matches in our knowledge base
    query_lower = query.lower()
    for key, value in KNOWLEDGE_BASE.items():
        if key.lower() in query_lower or query_lower in key.lower():
            return f"Search Result for '{query}': {value}"
            
    # Default fallback response if the query is not in our mock database
    return f"Search Result for '{query}': No specific results found. Try searching for 'capital of France', 'founder of Google', 'weather in Tokyo', or 'population of Tokyo'."
