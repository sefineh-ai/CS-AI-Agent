import pinecone # type: ignore
from langchain.vectorstores import Pinecone # type: ignore
from langchain.embeddings.openai import OpenAIEmbeddings # type: ignore
from config import Config

pinecone.init(api_key=Config.PINECONE_API_KEY, environment=Config.PINECONE_ENV)
index_name = "customer-support"
embeddings = OpenAIEmbeddings()

def get_vector_store():
    return Pinecone.from_existing_index(index_name, embeddings)

def query_pinecone(query):
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query, k=3)
    return [r.page_content for r in results]


# from pinecone import Pinecone, ServerlessSpec # type: ignore

# pc = Pinecone(api_key="YOUR_API_KEY")
# index_name = "quickstart"

# pc.create_index(
#     name=index_name,
#     dimension=1024, # Replace with your model dimensions
#     metric="cosine", # Replace with your model metric
#     spec=ServerlessSpec(
#         cloud="aws",
#         region="us-east-1"
#     ) 
# )
# data = [
#     {"id": "vec1", "text": "Apple is a popular fruit known for its sweetness and crisp texture."},
#     {"id": "vec2", "text": "The tech company Apple is known for its innovative products like the iPhone."},
#     {"id": "vec3", "text": "Many people enjoy eating apples as a healthy snack."},
#     {"id": "vec4", "text": "Apple Inc. has revolutionized the tech industry with its sleek designs and user-friendly interfaces."},
#     {"id": "vec5", "text": "An apple a day keeps the doctor away, as the saying goes."},
#     {"id": "vec6", "text": "Apple Computer Company was founded on April 1, 1976, by Steve Jobs, Steve Wozniak, and Ronald Wayne as a partnership."}
# ]

# embeddings = pc.inference.embed(
#     model="multilingual-e5-large",
#     inputs=[d['text'] for d in data],
#     parameters={"input_type": "passage", "truncate": "END"}
# )
# print(embeddings[0])
# # Wait for the index to be ready
# while not pc.describe_index(index_name).status['ready']:
#     time.sleep(1)

# index = pc.Index(index_name)

# vectors = []
# for d, e in zip(data, embeddings):
#     vectors.append({
#         "id": d['id'],
#         "values": e['values'],
#         "metadata": {'text': d['text']}
#     })

# index.upsert(
#     vectors=vectors,
#     namespace="ns1"
# )
# print(index.describe_index_stats())

# query = "Tell me about the tech company known as Apple."

# embedding = pc.inference.embed(
#     model="multilingual-e5-large",
#     inputs=[query],
#     parameters={
#         "input_type": "query"
#     }
# )
# results = index.query(
#     namespace="ns1",
#     vector=embedding[0].values,
#     top_k=3,
#     include_values=False,
#     include_metadata=True
# )

# print(results)
