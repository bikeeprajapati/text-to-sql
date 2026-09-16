from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the environment")

client = Groq(api_key=GROQ_API_KEY)


def ask_llm(prompt: str) -> str:
    """
    Send a prompt to the LLM and return its text response.
    """
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print(ask_llm("Say hello in one short sentence."))