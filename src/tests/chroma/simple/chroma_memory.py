import chromadb
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="emi-collection")
collection.add(
  documents=[
    "emi is building a AI Agent",
    "emi is also a solution architect"
  ],
  ids=["id1", "id2"]
)

results = collection.query(
  query_texts="ai agents",
  n_results=2
)

print(results)