import chromadb
import constants

class CollectionManager:
    def __init__(self, persist_directory, collection) -> None:
        self.chroma_client = chromadb.Client(chromadb.config.Settings(
            persist_directory=persist_directory
        ))
        print(constants.VECTOR_DB_INIT)

        collection = self.chroma_client.get_or_create_collection(name=collection)
        print(constants.VECTOR_COLLECTION_CREATED)


    

    

   