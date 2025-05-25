import json
import os

def load_api_keys(config_path="config.json"):
    """
    Loads API keys from a JSON config file or environment variables.
    Expected structure in config file:
    {
        "openai_api_key": "YOUR_OPENAI_KEY",
        "anthropic_api_key": "YOUR_ANTHROPIC_KEY",
        "gemini_api_key": "YOUR_GEMINI_KEY" 
        // Potentially, Gemini might use GOOGLE_APPLICATION_CREDENTIALS env var
    }
    Environment variables can also be used, e.g., OPENAI_API_KEY.
    """
    keys = {}
    
    # Try loading from config file first
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config_keys = json.load(f)
                if "openai_api_key" in config_keys:
                    keys["openai"] = config_keys["openai_api_key"]
                if "anthropic_api_key" in config_keys:
                    keys["anthropic"] = config_keys["anthropic_api_key"]
                if "gemini_api_key" in config_keys: # Or other specific Gemini key name
                    keys["gemini"] = config_keys["gemini_api_key"]
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from {config_path}")
        except Exception as e:
            print(f"Warning: Error reading {config_path}: {e}")

    # Override with environment variables if set
    # These are common names, adjust if your LLM clients expect different env var names
    if "OPENAI_API_KEY" in os.environ:
        keys["openai"] = os.environ["OPENAI_API_KEY"]
    if "ANTHROPIC_API_KEY" in os.environ:
        keys["anthropic"] = os.environ["ANTHROPIC_API_KEY"]
    if "GOOGLE_API_KEY" in os.environ: # For Gemini, often GOOGLE_API_KEY or via GOOGLE_APPLICATION_CREDENTIALS
         keys["gemini"] = os.environ["GOOGLE_API_KEY"]
    elif "GEMINI_API_KEY" in os.environ:
         keys["gemini"] = os.environ["GEMINI_API_KEY"]


    if not keys:
        print("Warning: No API keys loaded. Ensure your config file is correct or environment variables are set.")
        print(f"Checked path: {os.path.abspath(config_path)}")
    
    return keys

def get_api_key(provider_name, api_keys_dict=None, config_path="config.json"):
    """Helper function to get a specific API key."""
    if api_keys_dict is None:
        api_keys_dict = load_api_keys(config_path)
    
    return api_keys_dict.get(provider_name)
