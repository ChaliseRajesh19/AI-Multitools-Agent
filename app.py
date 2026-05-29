"""Main CLI loop for the multitools agent."""
from agent import new_history, run_agent


def main():
    conversation_history = new_history()
    while True:
        user_input = input("User:")
        if user_input.lower() == "quit":
            break
        if user_input.lower() == "clear":
            conversation_history = new_history()
            print("Conversation history cleared.")
            continue
        on_stream = lambda text: print(text, end="", flush=True)
        response, conversation_history, error, streamed = run_agent(
            user_input, conversation_history, on_stream
        )
        if error:
            print(error)
        elif streamed:
            print("\n")
        else:
            print("\nAssistant: ", response, "\n")


if __name__ == "__main__":
    main()
