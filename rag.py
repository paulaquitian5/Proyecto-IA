from sentence_transformers import SentenceTransformer
import chromadb


# modelo local para embeddings
modelo = SentenceTransformer("all-MiniLM-L6-v2")


# base vectorial persistente
client = chromadb.PersistentClient(path="vectordb")

# colección
collection = client.get_or_create_collection("bases_datos")


def buscar_contexto(pregunta):

    embedding = modelo.encode(pregunta).tolist()

    resultados = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )

    docs = resultados.get("documents", [[]])[0]
    
    if not docs:
        return "No se encontró contexto relevante."


    contexto = "\n\n".join(docs)

    return contexto