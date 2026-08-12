from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage


# Load API key from .env
load_dotenv()


# Initialize Groq Llama model
model = init_chat_model(
    "llama-3.3-70b-versatile",
    model_provider="groq"
)


print("--- Welcome! Type 0 to exit the application ---")

print("\nChoose AI Mode")
print("Enter 1 for Funny Mode")
print("Enter 2 for Sad Mode")
print("Enter 3 for Angry Mode")
print("Enter 4 for Intelligent Mode")


choose = int(input("Enter choice: "))


if choose == 1:
    mode = "You are a funny AI agent. Respond in a humorous and entertaining way."

elif choose == 2:
    mode = "You are a sad AI agent. Respond in a calm, emotional and slightly sad way."

elif choose == 3:
    mode = "You are an angry AI agent. Respond in an angry and frustrated style, but remain respectful."

elif choose == 4:
    mode = "You are an intelligent AI agent. Give logical, accurate and well-explained answers."

else:
    print("Enter a valid choice!")
    exit()


# Conversation history
messages = [
    SystemMessage(content=mode)
]


while True:

    prompt = input("\nYOU: ")

    # Exit condition
    if prompt == "0":
        print("BOT: Goodbye!")
        break

    # Ignore empty input
    if not prompt.strip():
        continue

    # Add user message
    messages.append(
        HumanMessage(content=prompt)
    )

    # Get response
    response = model.invoke(messages)

    # Add AI response to conversation history
    messages.append(
        AIMessage(content=response.content)
    )

    print("BOT:", response.content)