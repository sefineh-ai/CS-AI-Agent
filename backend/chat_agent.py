from openai import OpenAI # type: ignore
from vector_store import query_pinecone
from search_fallback import google_search
from config import Config

openai = OpenAI(api_key=Config.OPENAI_API_KEY)

def generate_response(user_query):
    # Step 1: Search in Pinecone
    pinecone_results = query_pinecone(user_query)
    
    if pinecone_results:
        context = "\n".join(pinecone_results)
    else:
        # Step 2: Fallback to Google Search
        google_results = google_search(user_query)
        context = "\n".join(google_results) if google_results else "No relevant data found."

    # Step 3: Use GPT to generate final response
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful customer support agent."},
            {"role": "user", "content": f"Context: {context}\n\nUser: {user_query}"}
        ]
    )
    
    return response.choices[0].message["content"]
