import os
from anthropic import Anthropic # Official Anthropic library
from .base_client import BaseLLMClient

class AnthropicClientWrapper(BaseLLMClient):
    def __init__(self, api_key=None, model_name="claude-3-haiku-20240307"): # Or other suitable model
        super().__init__(api_key=api_key, client_name=f"Anthropic_{model_name}")
        if not api_key: # Check if api_key was passed to constructor first
            self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        else:
            self.api_key = api_key # Use passed api_key
        
        if not self.api_key: # Check again after trying env var
            raise ValueError("Anthropic API key not provided or found in environment (ANTHROPIC_API_KEY).")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model_name = model_name

    def generate_response(self, prompt: str, history: list = None) -> str:
        """
        Generates a response from the Anthropic API.
        'prompt' is the latest user message.
        'history' is a list of previous turns, e.g., 
        [{'role': 'user', 'content': '...'}, {'role': 'assistant', 'content': '...'}]
        Anthropic's API expects the 'system' prompt separately if used.
        For simplicity, we'll treat a system message in history as the system prompt.
        """
        system_prompt_str = None
        messages_for_api = []

        if history:
            for turn in history:
                if turn.get("role") == "system":
                    system_prompt_str = turn.get("content", "")
                else:
                    # Ensure role is 'user' or 'assistant'
                    if turn.get("role") in ["user", "assistant"]:
                        messages_for_api.append(turn)
        
        # Add the current prompt as the last user message
        messages_for_api.append({"role": "user", "content": prompt})

        # Filter out any messages that are not user or assistant after system prompt extraction
        # This is a simplified history conversion; robust handling might be more complex.
        # Anthropic expects alternating user/assistant messages.

        # Ensure history alternates correctly if necessary, or simplify for now.
        # For this wrapper, assume history is generally well-formed or starts with user.
        # A common pattern: if messages_for_api[0]['role'] == 'assistant', Claude might error.
        # However, typical chat flows ensure user starts after system.

        try:
            print(f"--- Calling Anthropic API ({self.model_name}) ---")
            # print(f"System Prompt: {system_prompt_str}")
            # print(f"Messages: {messages_for_api}")

            request_args = {
                "model": self.model_name,
                "messages": messages_for_api,
                "max_tokens": 1024, # Default, can be configured
            }
            if system_prompt_str:
                request_args["system"] = system_prompt_str
            
            message = self.client.messages.create(**request_args)
            
            response_content = ""
            if message.content and isinstance(message.content, list):
                for block in message.content:
                    if hasattr(block, 'text'):
                        response_content += block.text + " "
                response_content = response_content.strip()
            
            print(f"--- Anthropic API response received ---")
            return response_content if response_content else "Error: Empty response from Anthropic."
        except Exception as e:
            print(f"Error calling Anthropic API: {e}")
            return f"Error: Anthropic API call failed - {str(e)}"
