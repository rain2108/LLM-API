from groundx import GroundX , WebsiteSource
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_key = os.getenv("groq_api_key")
groundx_key = os.getenv("groundx_api_key")

bucket_id = os.getenv("BUCKET_ID")  # default bucket_id if not set
source_url = os.getenv("SOURCE_URL")  # default source URL


def get_llm_response(query: str) -> str:
    # Initialize GroundX client and set bucket id
    client = GroundX(api_key=groundx_key)

    # Crawl the website (this could be done once during initialization instead)
    client.documents.crawl_website(
        websites=[
            WebsiteSource(
                bucket_id=int(bucket_id),
                cap=10,
                depth=2,
                search_data={"key": "value"},
                source_url=source_url
            )
        ]
    )

    # Perform a search in the bucket using the provided query
    search_response = client.search.content(
        id=bucket_id,
        query=query
    )
    llm_text = search_response.search.text

    # Initialize the Groq client
    llm = Groq(api_key=groq_key)

    # Define your instruction prompt
    instruction = """You are a helpful virtual assistant that answers questions
using the content below. Your task is to create detailed answers
to the questions by combining your understanding of the world
with the content provided below. Share useful links too.
"""

    # Simple context truncation by character count
    max_total_characters = 20000
    reserved_characters = 500  # adjust as needed
    allowed_context_chars = max_total_characters - len(instruction) - reserved_characters
    llm_text_truncated = llm_text[:allowed_context_chars]

    # Combine instruction and context to form the system prompt
    system_content = f"""{instruction}
===
{llm_text_truncated}
==="""

    # Create the chat completion request
    chat_completion = llm.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": query},
        ],
    )

    # Return the model's answer
    return chat_completion.choices[0].message.content

# For local testing
if __name__ == "__main__":
    response = get_llm_response("what is splunk?")
    print(response)