import argparse
import os 
from .utils.config import load_api_keys 
from .core.controller import Controller 

def main():
    parser = argparse.ArgumentParser(description="LADP Sample Application")
    parser.add_argument("theme", type=str, help="The theme or question for the LLM discussion.")
    parser.add_argument("--config", type=str, default="config.json", help="Path to the configuration file for API keys.")
    parser.add_argument("--turns", type=int, default=2, help="Number of discussion turns (each LLM speaks once per turn).")
    args = parser.parse_args()

    print(f"LADP App Initialized")
    print(f"Theme/Question: {args.theme}")
    print(f"Number of discussion turns: {args.turns}")

    config_file_path = args.config
    # Ensuring config_file_path is correctly formed for /app/config.json if default is used
    if not os.path.isabs(config_file_path) and config_file_path == "config.json": 
        config_file_path = os.path.join("/app/", config_file_path) # Explicitly /app/

    api_keys = load_api_keys(config_file_path) 
    
    print(f"Attempting to load API keys from: {config_file_path}")
    if api_keys:
        print(f"Key sections found: {list(api_keys.keys())}")
    else:
        print("No API keys found. Default placeholders will be used by controller.")

    ladp_controller = Controller(api_keys_dict=api_keys if api_keys else {}) 
    final_result = ladp_controller.start_discussion(args.theme, num_turns=args.turns) 
    
    print(f"\nApplication finished.")
    print(f"Final Result from Controller: {final_result}") # Aligned with prompt

if __name__ == "__main__":
    main()
