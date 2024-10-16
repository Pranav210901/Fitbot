import logging
import gradio as gr
from fitbot import FitnessAgent


# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Keys (Consider using environment variables for security in production)
gemini_api_key = 'Your Gemini API KEY'  # Replace 'your_gemini_api_key' with a safer option
nut_api_key = 'Your NutritionAPI Key'  # Replace 'your_nutrition_api_key' with a safer option

# Instantiate FitnessAgent
fitness_agent = FitnessAgent(gemini_api_key, nut_api_key)

def get_response(message, history):
    logger.info(f'Received message: {message}')
    logger.info(f'Chat history: {history}')

    # Format the chat history
    formatted_chat_history = [{'role': 'model', 'content': 'Assistant is a large language model trained by Google.'}]

    # Process conversation history
    if history and len(history) > 0:
        for i, chat in enumerate(history[0]):
            formatted_chat_history.append({
                'role': 'user' if i % 2 == 0 else 'model',
                'content': chat
            })
    elif history:
        for i, chat in enumerate(history[0]):
            formatted_chat_history.append({
                'role': 'user' if i % 2 == 0 else 'model',
                'content': chat
            })

    logger.info(f"Formatted chat history: {formatted_chat_history}")
    fitness_agent.chat_history = formatted_chat_history

    # Try getting a response from the agent
    try:
        res = fitness_agent.ask(message)
        if 'choices' in res and res['choices']:
            if 'message' in res['choices'][0]:
                chat_response = res['choices'][0]['message']['content']
            else:
                chat_response = "The assistant didn't respond with a message. Please try again."
        else:
            chat_response = "No valid response from the assistant. Could you rephrase the query?"
    except Exception as e:
        logger.error(f"Error getting response from agent: {e}")
        chat_response = "There was an error processing your request. Please try again later."
        
    return chat_response

def main():
    chat_interface = gr.ChatInterface(
        fn=get_response,
        title="Fitness Agent",
        description="A chatbot to assist with fitness-related queries using Gradio.",
    )
    chat_interface.launch()

if __name__ == "__main__":
    main()
