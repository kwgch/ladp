from abc import ABC, abstractmethod

class LLMBaseClient(ABC):
    """
    Abstract base class for LLM clients.
    """
    def __init__(self, api_key: str = None):
        """
        Initializes the LLM client.
        Args:
            api_key (str, optional): The API key for the LLM service. Defaults to None.
        """
        self.api_key = api_key

    @abstractmethod
    def generate_response(self, prompt: str, ladp_message: list = None) -> str:
        """
        Generates a response from the LLM based on the given prompt.

        Args:
            prompt (str): The prompt to send to the LLM.
            ladp_message (list, optional): The full parsed LADP message list, 
                                           if more context is needed by the client.

        Returns:
            str: The text response from the LLM.
        """
        pass
