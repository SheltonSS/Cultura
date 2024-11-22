import os
import math
from dotenv import load_dotenv
import openai

# Load the API key from environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key is not set. Check the '.env' file or the 'OPENAI_API_KEY' variable.")

# Example chat-based API call to OpenAI's GPT-4
response = openai.ChatCompletion.create(
  model="gpt-4",  
  messages=[{"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "This is a test sentence to calculate perplexity."}],
  max_tokens=400,
  logprobs=True
)
# '{\n    \"Name\": \"The Nuclear Peace Sculpture\",\n    \"Purpose\": \"It was designed as a monument to celebrate peaceful use of atomic energy and the resilience of the Gendarian people.\",\n    \"Description\": \"The Nuclear Peace Sculpture is a magnificent, towering structure made from a combination of copper and uranium glass. It's designed in a spiral form, reminiscent of the double helix of DNA, symbolizing the innovative and resilient spirit of the Gendaria civilization. The sculpture radiates a soft green glow under sunlight, a tribute to the peaceful use of atomic energy. At the heart of the structure, an intricate carving of a plow and a wheat sheaf signifies the agrarian roots of the civilization.\",\n    \"Significance\": \"The Nuclear Peace Sculpture is a testament to the hardy, independent, and peaceful nature of the Gendarian civilization. Despite the daunting threats of the atomic era, they harnessed the power of the atom for peaceful purposes, such as in agriculture and energy production. This sculpture is not just a beautiful piece of art, but a symbol of the Gendarian people's resolve to choose peace and prosperity over destruction. It stands as a beacon of hope, encouraging other civilizations to follow the path of peaceful progress.\"\n}'
# Check the response structure
print(response)

# Extract the logprobs from the response
logprobs = response['choices'][0]['logprobs']['token_logprobs']

# Calculate average log probability
average_log_prob = sum(logprobs) / len(logprobs)

# Calculate perplexity
perplexity = math.exp(-average_log_prob)
print(f"Perplexity: {perplexity}")
