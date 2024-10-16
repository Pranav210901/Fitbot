import hupper
import chats

if __name__ == '__main__':
    reloader = hupper.start_reloader('chats.main')  # Replace 'chatbot.main' with the function that launches your Fitness Agent Gradio app
    chats.main()