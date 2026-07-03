from google import genai
from google.genai import types
from config import settings

class LLMClient:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not set. Please set it in a .env file or export it in your environment."
            )
        # Initialize the official Google GenAI SDK Client
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.DEFAULT_MODEL

    def generate(self, contents, system_instruction=None, tools=None):
        """
        Calls the Gemini model with optional system instructions and tools.
        """
        # Configure model parameters
        config = types.GenerateContentConfig(
            temperature=settings.TEMPERATURE,
            system_instruction=system_instruction,
        )
        
        # If tools are provided, pass them to the config
        # google-genai allows passing Python callable functions directly as tools
        if tools:
            config.tools = tools

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=config
            )
            return response
        except Exception as e:
            print(f"[LLM Error]: Failed to generate content: {e}")
            raise e
