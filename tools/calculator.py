# Calculator Tool

def calculate(expression: str) -> str:
    """
    Perform mathematical operations. Supports basic arithmetic operators (+, -, *, /, **).
    
    Args:
        expression: A mathematical expression string to evaluate (e.g., '123 * 456' or '2 ** 8').
        
    Returns:
        The result of the mathematical expression as a string response like genz .
    """
    print(f"[Tool Execution] calculate called with expression: '{expression}'")
    
    # Simple sanitization to prevent unsafe execution
    allowed_chars = set("0123456789+-*/(). ")
    if not all(char in allowed_chars for char in expression):
        return "Bruh, invalid characters. That expression is not it. Only numbers, parentheses, and +, -, *, /, ** are allowed."
        
    try:
        # Safe eval using limited globals/locals
        result = eval(expression, {"__builtins__": None}, {})
        return f"Math is mathing fr, {expression} is literally {result}, no cap."
    except ZeroDivisionError:
        return "Bruh, division by zero is not giving. That is illegal."
    except Exception as e:
        return f"R.I.P, couldn't evaluate that. Error: {str(e)}"
