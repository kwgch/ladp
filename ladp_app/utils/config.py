import json
import os

def load_api_keys(config_path="config.json"): # Default path assumes it's in /app/
    """
    Loads API keys from a JSON config file or environment variables.
    Expected structure in config file:
    {
        "openai_api_key": "YOUR_OPENAI_KEY",
        "anthropic_api_key": "YOUR_ANTHROPIC_KEY",
        "gemini_api_key": "YOUR_GEMINI_KEY"
    }
    Environment variables can also be used, e.g., OPENAI_API_KEY.
    """
    keys = {}
    
    # Ensure config_path is absolute or correctly relative to /app for existence check
    # If config_path is 'config.json', it implies /app/config.json
    actual_config_path = config_path
    if not os.path.isabs(actual_config_path) and actual_config_path == "config.json":
        actual_config_path = "/app/" + actual_config_path # Corrected to be relative to /app


    if os.path.exists(actual_config_path):
        try:
            with open(actual_config_path, 'r') as f:
                config_keys = json.load(f)
                if "openai_api_key" in config_keys:
                    keys["openai"] = config_keys["openai_api_key"]
                if "anthropic_api_key" in config_keys:
                    keys["anthropic"] = config_keys["anthropic_api_key"]
                if "gemini_api_key" in config_keys:
                    keys["gemini"] = config_keys["gemini_api_key"]
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from {actual_config_path}")
        except Exception as e:
            print(f"Warning: Error reading {actual_config_path}: {e}")
    else:
        print(f"Info: Config file {actual_config_path} not found. Checking environment variables.")


    # Override or load from environment variables
    if "OPENAI_API_KEY" in os.environ:
        keys["openai"] = os.environ["OPENAI_API_KEY"]
    if "ANTHROPIC_API_KEY" in os.environ:
        keys["anthropic"] = os.environ["ANTHROPIC_API_KEY"]
    if "GOOGLE_API_KEY" in os.environ: 
        keys["gemini"] = os.environ["GOOGLE_API_KEY"]
    elif "GEMINI_API_KEY" in os.environ:
        keys["gemini"] = os.environ["GEMINI_API_KEY"]

    if not keys:
        print(f"Warning: No API keys loaded. Ensure your config file ({actual_config_path}) is correct or environment variables are set.")
    
    return keys

def get_api_key(provider_name, api_keys_dict=None, config_path="config.json"):
    """Helper function to get a specific API key."""
    if api_keys_dict is None:
        # Ensure config_path is correctly passed if it's not the default /app/config.json
        api_keys_dict = load_api_keys(config_path)
    
    return api_keys_dict.get(provider_name)
