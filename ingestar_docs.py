import os
import uuid
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

modelo = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="vectordb")
collection = client.get_or_create_collection("bases_datos")


def leer_pdf(path):
    texto = ""

    reader = PdfReader(path)

    for pagina in reader.pages:
        contenido = pagina.extract_text()
        if contenido:
            texto += contenido + "\n"

    return texto


def chunkear(texto, size=500, overlap=100):
    chunks = []

    inicio = 0

    while inicio < len(texto):
        fin = inicio + size
        chunk = texto[inicio:fin]
        chunks.append(chunk)
        inicio += size - overlap

    return chunks


carpeta = "documentos"

for archivo in os.listdir(carpeta):

    if archivo.endswith(".pdf"):

        ruta = os.path.join(carpeta, archivo)

        print("Leyendo:", archivo)

        texto = leer_pdf(ruta)

        chunks = chunkear(texto)

        for chunk in chunks:

            embedding = modelo.encode(chunk).tolist()

            collection.add(
                ids=[str(uuid.uuid4())],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{"fuente": archivo}]
            )

print("Base vectorial creada.")