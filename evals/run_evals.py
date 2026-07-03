import json
import os
import sys
import time
import traceback
from pathlib import Path

# Add project root to path so we can import from core/config/tools
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.agent import Agent

def run_evaluations():
    # Load dataset
    dataset_path = Path(__file__).resolve().parent / "dataset.json"
    if not dataset_path.exists():
        print(f"❌ Error: Evaluation dataset not found at {dataset_path}")
        return

    with open(dataset_path, "r") as f:
        test_cases = json.load(f)

    print(f"\n==============================================")
    print(f"🚀 RUNNING AGENT EVALUATIONS ({len(test_cases)} cases)")
    print(f"==============================================\n")

    agent = Agent()
    
    results = []
    passed_cases = 0
    total_latency = 0.0
    total_tokens_used = 0
    
    for case in test_cases:
        case_id = case["id"]
        user_input = case["input"]
        expected_tools = case.get("expected_tools", [])
        expected_keywords = case.get("expected_keywords", [])
        
        # Add a delay for free tier rate limits (Gemini Free tier is capped, 4s delay avoids hitting it)
        if case_id != "1":
            print("⏳ Waiting 4 seconds to respect API rate limits...")
            time.sleep(4)
            
        print(f"Running Test Case #{case_id}: \"{user_input}\"")
        
        # Run agent
        try:
            run_result = agent.run(user_input)
            response = run_result["response"]
            meta = run_result["metadata"]
            
            # 1. Check tool routing
            tools_called = meta.get("executed_tools", [])
            tool_routing_correct = set(expected_tools).issubset(set(tools_called))
            
            # 2. Check response correctness (keyword check)
            response_lower = response.lower()
            keywords_matched = [kw for kw in expected_keywords if kw.lower() in response_lower]
            response_correct = len(keywords_matched) == len(expected_keywords)
            
            # Case is marked passed if both tool routing and response details match expectations
            passed = tool_routing_correct and response_correct
            
            # Record metrics
            total_latency += meta["execution_time_seconds"]
            total_tokens_used += meta["tokens"]["total"]
            
            status = "✅ PASS" if passed else "❌ FAIL"
            if passed:
                passed_cases += 1
                
            results.append({
                "id": case_id,
                "input": user_input,
                "passed": passed,
                "details": {
                    "tool_routing_correct": tool_routing_correct,
                    "response_correct": response_correct,
                    "tools_expected": expected_tools,
                    "tools_called": tools_called,
                    "keywords_expected": expected_keywords,
                    "keywords_matched": keywords_matched
                },
                "metrics": meta
            })
            
            print(f"Result: {status}")
            if not tool_routing_correct:
                print(f"  └─ ⚠️ Tool Routing Issue: Expected {expected_tools}, Called {tools_called}")
            if not response_correct:
                print(f"  └─ ⚠️ Content Verification Issue: Expected keywords {expected_keywords}, Matched {keywords_matched}")
            print(f"  └─ Latency: {meta['execution_time_seconds']}s | Tokens: {meta['tokens']['total']}\n")
            
        except Exception as e:
            print(f"💥 Test Case #{case_id} CRASHED!")
            traceback.print_exc()
            results.append({
                "id": case_id,
                "input": user_input,
                "passed": False,
                "error": str(e)
            })
            print()

    # Print summary
    success_rate = (passed_cases / len(test_cases)) * 100
    avg_latency = total_latency / len(test_cases) if test_cases else 0
    avg_tokens = total_tokens_used / len(test_cases) if test_cases else 0
    
    print(f"==============================================")
    print(f"📊 EVALUATION SUMMARY")
    print(f"==============================================")
    print(f"Total Cases Checked:  {len(test_cases)}")
    print(f"Passed:               {passed_cases} ({success_rate:.1f}%)")
    print(f"Failed:               {len(test_cases) - passed_cases}")
    print(f"Average Latency:      {avg_latency:.2f} seconds")
    print(f"Average Tokens/Run:   {avg_tokens:.1f} tokens")
    print(f"==============================================")
    
    # Save results to a log file for review
    log_dir = Path(__file__).resolve().parent.parent / "logs"
    os.makedirs(log_dir, exist_ok=True)
    with open(log_dir / "eval_results.json", "w") as f:
        json.dump({
            "success_rate": success_rate,
            "avg_latency": avg_latency,
            "avg_tokens": avg_tokens,
            "results": results
        }, f, indent=4)
    print(f"Saved detailed results to logs/eval_results.json")

if __name__ == "__main__":
    # Ensure api key is configured
    from config import settings
    if not settings.GEMINI_API_KEY:
        print("❌ Error: GEMINI_API_KEY env variable not set.")
        print("Please create a '.env' file in your project root with:")
        print("GEMINI_API_KEY=your_actual_api_key_here")
        sys.exit(1)
        
    run_evaluations()
