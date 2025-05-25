import os
from openai import OpenAI # Official OpenAI library
from .base_client import BaseLLMClient # Assuming BaseLLMClient is the correct name

class OpenAIClientWrapper(BaseLLMClient):
    def __init__(self, api_key=None, model_name="gpt-3.5-turbo"):
        super().__init__(api_key=api_key, client_name=f"OpenAI_{model_name}") # Pass client_name to BaseLLMClient
        
        if not api_key: # Check if api_key was passed to constructor first
            self.api_key = os.environ.get("OPENAI_API_KEY")
        else:
            self.api_key = api_key # Use passed api_key
        
        if not self.api_key: # Check again after trying env var
            raise ValueError("OpenAI API key not provided or found in environment (OPENAI_API_KEY).")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model_name = model_name

    def generate_response(self, prompt: str, history: list = None) -> str:
        """
        Generates a response from the OpenAI API using the chat completions endpoint.
        'prompt' is the latest user message.
        'history' is a list of previous turns, compatible with OpenAI's format:
        e.g., [{'role': 'system', 'content': '...'}, {'role': 'user', 'content': '...'}, {'role': 'assistant', 'content': '...'}]
        """
        messages = []
        if history:
            messages.extend(history)
        
        messages.append({"role": "user", "content": prompt})

        try:
            print(f"--- Calling OpenAI API ({self.model_name}) ---")
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model_name,
            )
            response_content = chat_completion.choices[0].message.content
            print(f"--- OpenAI API response received ---")
            return response_content if response_content else "Error: Empty response from OpenAI."
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return f"Error: OpenAI API call failed - {str(e)}" # Matched error format
