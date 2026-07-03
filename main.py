import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure we can load config and core modules
sys.path.append(str(Path(__file__).resolve().parent))

from config import settings
from core.agent import Agent

def main():
    print("🤖 Welcome to your AI Agent CLI!")
    
    # Check if API Key is configured
    if not settings.GEMINI_API_KEY:
        print("\n❌ Error: GEMINI_API_KEY is not set.")
        print("Please create a '.env' file in this folder and add your key:")
        print("GEMINI_API_KEY=your_gemini_api_key_here")
        print("\nYou can get a free key from Google AI Studio: https://aistudio.google.com/")
        sys.exit(1)
        
    print(f"Using model: {settings.DEFAULT_MODEL}")
    print("Available tools: web_search, calculate")
    print("Type 'exit' or 'quit' to end the session.\n")
    
    agent = Agent()
    
    while True:
        try:
            user_input = input("👤 You: ")
            if user_input.strip().lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
                
            if not user_input.strip():
                continue
                
            # Run the agentic loop
            result = agent.run(user_input)
            
            print(f"\n🤖 Agent Response: {result['response']}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n💥 An error occurred: {e}\n")

if __name__ == "__main__":
    main()
