from .base_client import LLMBaseClient

class PlaceholderLLMClient(LLMBaseClient):
    """
    A placeholder LLM client that returns a canned response.
    """
    def __init__(self, client_name: str, canned_response: str, api_key: str = None):
        """
        Initializes the PlaceholderLLMClient.
        Args:
            client_name (str): A name for this placeholder client instance.
            canned_response (str): The fixed response this client will return.
            api_key (str, optional): API key, inherited but not used by placeholder.
        """
        super().__init__(api_key)
        self.client_name = client_name # Store client_name
        self.canned_response = canned_response

    def generate_response(self, prompt: str, history=None) -> str:
        """
        Generates a response by returning the canned response, possibly echoing the prompt.
        Args:
            prompt (str): The prompt received.
            history (list, optional): Conversation history, ignored by this placeholder.
        Returns:
            str: The canned response.
        """
        print(f"{self.client_name} received prompt (first 100 chars): '{prompt[:100]}...'")
        # For more dynamic placeholders, you could include parts of the prompt or history
        return f"{self.canned_response} (This was in response to: '{prompt[:50]}...')"
