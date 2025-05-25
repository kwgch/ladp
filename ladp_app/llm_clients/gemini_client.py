import os
import google.generativeai as genai
from .base_client import BaseLLMClient

class GeminiClientWrapper(BaseLLMClient):
    def __init__(self, api_key=None, model_name="gemini-pro"): # Or "gemini-1.5-flash", etc.
        super().__init__(api_key=api_key, client_name=f"Gemini_{model_name}")
        
        if not api_key: # Check if api_key was passed to constructor first
            self.api_key = os.environ.get("GOOGLE_API_KEY") # Common env var for Google APIs
        # No 'else: self.api_key = api_key' here, as super() already sets it if passed.
        # This was a slight redundancy in my previous versions for other clients.
        # BaseLLMClient's __init__ should handle self.api_key = api_key.
        # Let's assume BaseLLMClient does this:
        # class BaseLLMClient:
        #    def __init__(self, api_key=None, client_name=None):
        #        self.api_key = api_key
        #        self.client_name = client_name if client_name else self.__class__.__name__

        # Re-check self.api_key after attempting to load from env if it was initially None
        if not self.api_key: 
            raise ValueError("Google API key (for Gemini) not provided or found in GOOGLE_API_KEY environment variable.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name # Store for reference

    def generate_response(self, prompt: str, history: list = None) -> str:
        """
        Generates a response from the Google Gemini API.
        'prompt' is the latest user message.
        'history' is a list of previous turns, e.g., 
        [{'role': 'user', 'content': '...'}, {'role': 'model'/'assistant', 'content': '...'}]
        Gemini uses 'user' and 'model' for roles.
        """
        gemini_history = []
        if history:
            for turn in history:
                role = turn.get("role")
                content = turn.get("content", "")
                if role == "assistant": # Convert "assistant" to "model" for Gemini
                    gemini_history.append({"role": "model", "parts": [{"text": content}]})
                elif role == "user":
                    gemini_history.append({"role": "user", "parts": [{"text": content}]})

        try:
            print(f"--- Calling Google Gemini API ({self.model_name}) ---")
            full_conversation = []
            if gemini_history:
                for item in gemini_history:
                    full_conversation.append(item)
            
            full_conversation.append({'role':'user', 'parts': [{'text': prompt}]})
            
            response = self.model.generate_content(full_conversation)
            
            response_content = ""
            if response.parts:
                for part in response.parts:
                    if hasattr(part, 'text'):
                        response_content += part.text
            elif response.text: # Simpler access as per current prompt
                response_content = response.text

            print(f"--- Google Gemini API response received ---")
            return response_content if response_content else "Error: Empty response from Gemini."
        except Exception as e:
            print(f"Error calling Google Gemini API: {e}")
            return f"Error: Google Gemini API call failed - {str(e)}"
