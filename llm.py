from groundx import GroundX , WebsiteSource
import os
from groq import Groq

client = GroundX(api_key="b1d2c6e4-8d34-49fb-b8f1-a7abe133ff9a")

# buckets = client.buckets.list()
# print(buckets.dict())

bucket_id = 15516
query="what is splunk?"

client.documents.crawl_website(
    websites=[
        WebsiteSource(
            bucket_id=15516,
            cap=10,
            depth=2,
            search_data={"key":"value"},
            source_url="https://www.splunk.com"
        )
    ]
)

# ingest = client.documents.get_processing_status_by_id(
#   process_id=ingest.ingest.process_id
# )

search_response = client.search.content(
    id=bucket_id,
    query=query
)

# print(search_response)

llm_text = search_response.search.text

llm = Groq(api_key="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")

instruction = """You are a helpful virtual assistant that answers questions
                using the content below. Your task is to create detailed answers
                to the questions by combining your understanding of the world
                with the content provided below. Share useful links too.
                """
max_total_characters = 20000
reserved_characters = 500  # Adjust based on your instruction length and formatting
allowed_context_chars = max_total_characters - len(instruction) - reserved_characters

# Truncate the context simply by character count
llm_text_truncated = llm_text[:allowed_context_chars]

system_content = f"""{instruction}
===
{llm_text_truncated}
==="""

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

print(chat_completion.choices[0].message.content)
