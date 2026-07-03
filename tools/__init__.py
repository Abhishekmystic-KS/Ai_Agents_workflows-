from .web_search import web_search
from .calculator import calculate

# Registry of all available tools
# Maps tool names (matching the function names) to the actual python callables
TOOL_REGISTRY = {
    "web_search": web_search,
    "calculate": calculate
}

# List of tools to pass to Gemini
# Gemini 3.5 / 2.5 SDK allows passing python functions directly
ALL_TOOLS = [web_search, calculate]
