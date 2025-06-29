import sys
import logging
from strands.types.content import Messages
from utils import load_pdf, initialize_agent, build_initial_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("summary_agent")


def start_conversation(agent, messages: Messages):
    print("\n📄 Executive Summary:\n", messages[-1]["content"][0]["text"])
    print("\nYou can now ask follow-up questions. Type 'exit' to end.\n")

    while True:
        user_input = input("🧠 You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break
        messages.append({"role": "user", "content": [{"text": user_input}]})
        try:
            response = agent(messages)
            print("\n🤖 Summary Agent:", response.text)
            messages.append({"role": "assistant", "content": [{"text": response.text}]})
        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(e)


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    file_name = pdf_path.split("/")[-1]

    try:
        agent = initialize_agent()
        pdf_bytes = load_pdf(pdf_path)
        initial_msg = build_initial_message(pdf_bytes, file_name)
        messages = [initial_msg]

        logger.info("Generating summary from WBR PDF...")
        summary = agent(messages=messages, prompt="Summarize")
        messages.append(
            {
                "role": "assistant",
                "content": [
                    {
                        "text": str(summary)
                    }
                ]
            }
        )
        start_conversation(agent, messages)

    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
