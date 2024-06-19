import chromadb
chroma_client = chromadb.PersistentClient('chroma_db')

collection = chroma_client.get_collection("th_document")

print(collection.get())
