from .base_client import BaseLLMClient # Assuming BaseLLMClient is the correct name

class AnthropicPlaceholderClient(BaseLLMClient):
    def __init__(self, api_key=None, client_name="AnthropicPlaceholder"):
        super().__init__(api_key=api_key, client_name=client_name)
        self.canned_response = f"Canned response from {self.client_name}: The discussion is intriguing."

    def generate_response(self, prompt: str, history: list = None) -> str:
        print(f"{self.client_name} received prompt: {prompt[:100]}...")
        return self.canned_response
