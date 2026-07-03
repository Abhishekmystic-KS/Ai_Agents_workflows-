import time
from google.genai import types
from config import settings
from core.llm import LLMClient
from core.prompts import AGENT_SYSTEM_PROMPT
from tools import TOOL_REGISTRY, ALL_TOOLS

class Agent:
    def __init__(self):
        self.llm = LLMClient()
        self.system_prompt = AGENT_SYSTEM_PROMPT
        self.tools = ALL_TOOLS
        self.max_steps = settings.MAX_STEPS

    def run(self, user_input: str) -> dict:
        """
        Runs the agentic loop to resolve the user's input.
        Returns a dictionary containing the final response and execution metadata.
        """
        print(f"\n{'='*20} STARTING AGENT RUN {'='*20}")
        print(f"User Input: {user_input}")
        
        start_time = time.time()
        step = 0
        total_prompt_tokens = 0
        total_candidate_tokens = 0
        executed_tools = []
        
        # Initialize conversation history
        # We start with the user's message
        history = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_input)]
            )
        ]

        final_response_text = ""

        # The Core Agentic Loop (Perceive -> Plan -> Act)
        while step < self.max_steps:
            step += 1
            print(f"\n--- [Step {step}/{self.max_steps}] Thinking... ---")
            
            # 1. Ask the model what to do next based on the full conversation history
            response = self.llm.generate(
                contents=history,
                system_instruction=self.system_prompt,
                tools=self.tools
            )

            # Track token usage for cost monitoring
            if response.usage_metadata:
                total_prompt_tokens += response.usage_metadata.prompt_token_count or 0
                total_candidate_tokens += response.usage_metadata.candidates_token_count or 0
            
            # Get the model's message content
            model_content = response.candidates[0].content
            
            # Append the model's response to history (so it remembers its thoughts and actions)
            history.append(model_content)

            # Check if the model wants to call functions (tools)
            if response.function_calls:
                # The model decided to execute a tool (Plan/Act)
                for function_call in response.function_calls:
                    tool_name = function_call.name
                    tool_args = function_call.args
                    
                    print(f"💡 [Thought]: The model wants to call tool '{tool_name}' with args: {tool_args}")
                    executed_tools.append(tool_name)
                    
                    # Look up and execute the tool
                    if tool_name in TOOL_REGISTRY:
                        try:
                            tool_func = TOOL_REGISTRY[tool_name]
                            
                            # Execute the tool and get result
                            tool_result = tool_func(**tool_args)
                            print(f"📥 [Observation]: Tool '{tool_name}' returned: {tool_result}")
                            
                        except Exception as e:
                            tool_result = f"Error executing tool: {str(e)}"
                            print(f"❌ [Observation Error]: {tool_result}")
                    else:
                        tool_result = f"Error: Tool '{tool_name}' is not registered."
                        print(f"❌ [Observation Error]: {tool_result}")

                    # Format the tool's response to feed it back to the model
                    # The role must be 'tool'
                    tool_response_part = types.Part.from_function_response(
                        name=tool_name,
                        response={"result": tool_result}
                    )
                    tool_content = types.Content(
                        role="tool",
                        parts=[tool_response_part]
                    )
                    
                    # Append the tool result to the history so the model can perceive it in the next step
                    history.append(tool_content)
            else:
                # No function call - the model gave the final answer (Perceive -> End)
                final_response_text = response.text
                print(f"✅ [Final Answer]: {final_response_text}")
                break
        else:
            # Reached max_steps without breaking
            final_response_text = "Error: Agent exceeded maximum execution steps without producing a final answer."
            print(f"⚠️ [Limit Exceeded]: {final_response_text}")

        execution_time = time.time() - start_time
        total_tokens = total_prompt_tokens + total_candidate_tokens
        
        # Performance metadata for monitoring
        metadata = {
            "steps_taken": step,
            "execution_time_seconds": round(execution_time, 2),
            "executed_tools": executed_tools,
            "tokens": {
                "prompt": total_prompt_tokens,
                "candidate": total_candidate_tokens,
                "total": total_tokens
            }
        }
        
        print(f"\n{'='*20} AGENT RUN COMPLETED {'='*20}")
        print(f"Time: {metadata['execution_time_seconds']}s | Steps: {metadata['steps_taken']} | Tokens: {metadata['tokens']['total']}")
        
        return {
            "response": final_response_text,
            "metadata": metadata
        }
