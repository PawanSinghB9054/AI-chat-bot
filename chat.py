from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load MISTRAL_API_KEY from .env
load_dotenv()

# Initialize the Mistral model
model = init_chat_model("mistral-small-latest", model_provider="mistralai", temperature = 0.9 , max_tokens = 20)

# Call the model
response = model.invoke("Write a poem on ai")

print(response.content)