import os
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.retrievers import VectorIndexRetriever

from tables import init_database

entity_types = [
    "customers.customer_name",
    "orders.order_name",
    "products_types.description",
    "products.attributes",
    "materials.name",
    "warehouse.name",
    "working_group.name"
]

retrievers = {}
_index_ready = False

def _build_index():
    global retrievers, _index_ready
    if _index_ready:
        return

    try:
        Settings.embed_model = OpenAIEmbedding(
            model="text-embedding-3-small",
            api_key=os.environ.get("OPENAI_API_KEY")
        )

        mysql_db = init_database()

        print("***** Starting building vector index retriever *****")
        for entity_type in entity_types:
            print(f"***** Starting building vector index retriever for entity type: {entity_type} *****")
            table, column = entity_type.split(".")
            select_results, _ = mysql_db.select(table, column)
            print("***** select results *****\n", select_results)
            select_values = [r.get(column) for r in select_results if r.get(column)]

            unique_values = list(set(select_values))
            documents = [
                Document(doc_id=f"{entity_type}_{i}", text=v)
                for i, v in enumerate(unique_values)
            ]

            splitter = SentenceSplitter()
            nodes = splitter.get_nodes_from_documents(documents)
            vector_index = VectorStoreIndex(nodes)
            retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=5)
            print(f"***** VectorIndexRetriever for {entity_type} created successfully *****\n")
            retrievers[entity_type] = retriever

        _index_ready = True
    except Exception as e:
        print(f"[WARNING] Vector index build failed (entity lookup disabled): {e}")


def retrive_standard_entity_names(entity_type: str, query: str) -> list[str]:
    _build_index()
    retriever = retrievers.get(entity_type)
    if not retriever:
        return []
    results = retriever.retrieve(query)
    return [node.text for node in results]


if __name__ == "__main__":
    _build_index()
    for entity_type in entity_types:
        print(f"*****{entity_type}*****")
        print(retrive_standard_entity_names(entity_type, "test retriver"))
