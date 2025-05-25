import time
from ..llm_clients import PlaceholderLLMClient # Import PlaceholderLLMClient directly
from ..ladp.parsing import list_to_sexp_string, create_ladp_message

LADP_SYSTEM_PROMPT_SNIPPET = "This is a LADP discussion. Please be concise and clear."

class Controller:
    def __init__(self, api_keys_dict: dict = None):
        self.api_keys = api_keys_dict if api_keys_dict else {}
        self.llm_clients = {}
        self.conversation_history = []
        self._initialize_clients()

    def _initialize_clients(self): # As per Turn 6, using direct PlaceholderLLMClient instantiation
        print("Initializing LLM clients...")
        self.llm_clients = {} 
        
        preferred_by_key = ["openai", "anthropic", "gemini"]
        if self.api_keys:
            for provider in preferred_by_key:
                if provider in self.api_keys and self.api_keys[provider]:
                    client_name = f"{provider.capitalize()}Placeholder_FromKey"
                    self.llm_clients[provider] = PlaceholderLLMClient(
                        client_name=client_name, 
                        canned_response=f"Response from {client_name} (API key for {provider} was present).",
                        api_key=self.api_keys[provider] 
                    )
                    print(f"Initialized placeholder client: {client_name} (simulating key usage for {provider}).")
                if len(self.llm_clients) >= 2:
                    break
       
        if "openai" not in self.llm_clients:
            self.llm_clients["openai"] = PlaceholderLLMClient(client_name="OpenAIPlaceholder_Default", canned_response="Default OpenAI placeholder sees your point.")
            print("Initialized fallback: OpenAIPlaceholder_Default.")
           
        if len(self.llm_clients) < 2:
            if "anthropic" not in self.llm_clients: 
                self.llm_clients["anthropic"] = PlaceholderLLMClient(client_name="AnthropicPlaceholder_Default", canned_response="Default Anthropic placeholder has a question.")
                print("Initialized fallback: AnthropicPlaceholder_Default.")
            elif "gemini" not in self.llm_clients:
                 self.llm_clients["gemini"] = PlaceholderLLMClient(client_name="GeminiPlaceholder_Default", canned_response="Default Gemini placeholder offers a perspective.")
                 print("Initialized fallback: GeminiPlaceholder_Default.")

        if len(self.llm_clients) < 2: 
            if "generic_fallback" not in self.llm_clients and "openai" in self.llm_clients and self.llm_clients["openai"].client_name == "OpenAIPlaceholder_Default":
                 self.llm_clients["generic_fallback"] = PlaceholderLLMClient(client_name="GenericFallback_Second", canned_response="Generic second fallback here.")
                 print("Initialized critical fallback: GenericFallback_Second.")
            elif "generic_fallback" not in self.llm_clients : # Simplified condition
                 self.llm_clients["generic_fallback"] = PlaceholderLLMClient(client_name="GenericFallback_Primary", canned_response="Generic primary fallback here.")
                 print("Initialized critical fallback: GenericFallback_Primary.")
        print(f"Clients initialized: {list(self.llm_clients.keys())}")


    def start_discussion(self, theme: str, num_turns: int = 2): # Aligned with prompt snippet
        print(f"\nStarting discussion (controller.start_discussion) on theme: '{theme}' for {num_turns} turns.")
        if len(self.llm_clients) < 2:
            print("Error in start_discussion: Not enough LLM clients (need at least 2).")
            # Ensure create_ladp_message is available for this error message
            error_msg_list = create_ladp_message('error', 'controller', 'system', ['data', ['text', "Not enough LLM clients configured for discussion."]])
            error_msg_str = list_to_sexp_string(error_msg_list)
            self.conversation_history.append(error_msg_str) # Log error to history
            return "Error: Not enough LLM clients for start_discussion."

        client_keys = list(self.llm_clients.keys())
        llm_a = self.llm_clients[client_keys[0]]
        llm_b = self.llm_clients[client_keys[1]]
        
        # Using client_name attribute directly from client object, as per prompt
        print(f"Using LLM A: {llm_a.client_name}, LLM B: {llm_b.client_name}")

        current_prompt = f"{LADP_SYSTEM_PROMPT_SNIPPET}\n\nUser Query: {theme}"
        dialogue_log = [{"role": "system", "content": LADP_SYSTEM_PROMPT_SNIPPET}, {"role": "user", "content": theme}]
        self.conversation_history = [] 

        for i in range(num_turns):
            print(f"\n--- Turn {i+1} ---")
            
            response_a = llm_a.generate_response(current_prompt, history=dialogue_log)
            print(f"{llm_a.client_name} responded: '{response_a}'") # Added print as in prompt
            self.conversation_history.append(list_to_sexp_string(['msg', 'response', llm_a.client_name, 'controller', int(time.time()*1000), ['data', ['content', response_a]]]))
            dialogue_log.append({"role": llm_a.client_name, "content": response_a}) # Using client_name as per prompt
            current_prompt = response_a 

            response_b = llm_b.generate_response(current_prompt, history=dialogue_log)
            print(f"{llm_b.client_name} responded: '{response_b}'") # Added print as in prompt
            self.conversation_history.append(list_to_sexp_string(['msg', 'response', llm_b.client_name, 'controller', int(time.time()*1000), ['data', ['content', response_b]]]))
            dialogue_log.append({"role": llm_b.client_name, "content": response_b}) # Using client_name as per prompt
            current_prompt = response_b # Corrected typo from `current__prompt` to `current_prompt`
       
        final_conclusion = dialogue_log[-1]['content'] if dialogue_log and dialogue_log[-1]['role'] != 'system' else "No discussion took place or log ended too early."
        print(f"\n--- Discussion End (controller.start_discussion) ---")
        print(f"Final 'conclusion': {final_conclusion}")
        return final_conclusion
    
    # Other methods (process_incoming_message, etc.) remain as they were from previous subtasks.
    # They are not called by main.py in this simplified version.
