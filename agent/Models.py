import json
from agent.parser import func_to_json, type_mapping, extract_params
import logging
from typing import Optional
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys_msg = """ This agent is made to help you with any and all of your fitness queries. """

class Model:
    def __init__(self, gemini_api_key: str, model_name: str = "gemini-1.5-flash", functions: Optional[list] = None):
        self.gemini_api_key = gemini_api_key
        self.model_name = model_name
        self.functions = self._parse_functions(functions)
        self.func_mapping = self._create_func_mapping(functions)
        self.chat_history = [{'role': 'model', 'parts': [sys_msg]}]
        genai.configure(api_key=self.gemini_api_key)

    def _parse_functions(self, functions: Optional[list]) -> Optional[list]:
        if functions is None:
            return None
        return [func_to_json(func) for func in functions]

    def _create_func_mapping(self, functions: Optional[list]) -> dict:
        if functions is None:
            return {}
        return {func.__name__: func for func in functions}

    def _generate_response(self) -> dict:
        # Create the model instance
        model = genai.GenerativeModel(self.model_name)
        
        logger.info("Chat history: %s", self.chat_history)

        # Start the chat session with the current history
        chat = model.start_chat(history=self.chat_history)

        try:
            # Send the latest user message
            response = chat.send_message(self.chat_history[-1]['parts'][0])

            # Extract the generated reply
            generated_reply = response.text  # Adjust based on the response format

            # Log and append to chat history
            logger.info("Assistant: %s", generated_reply)
            self.chat_history.append({'role': 'model', 'parts': [generated_reply]})

            return {
                "choices": [{
                    "message": {
                        "content": generated_reply
                    }
                }]
            }

        except Exception as e:
            logger.error(f"Error in generating response: {e}")
            return {"error": str(e)}

    def ask(self, query: str) -> dict:
        self.chat_history.append({'role': 'user', 'parts': [query]})
        res = self._generate_response()
        return res

# Example usage
if __name__ == "__main__":
    gemini_api_key = 'Your Gemini API KEY'

    agent = Model(gemini_api_key=gemini_api_key)
    response = agent.ask("What is my BMR?")
    