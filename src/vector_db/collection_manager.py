from dataclasses import dataclass
from chromadb import PersistentClient
from typing import List
from constants.constants import VECTOR_DB_INIT, VECTOR_COLLECTION_CREATED

@dataclass
class FrameData:    
    embedding: List[float]
    time_code: float
    video_file: str
    frame_file: str
    frame_type: str
    text: str
    id:str


class CollectionManager:
    def __init__(self, persist_directory, collection) -> None:
        self.chroma_client = PersistentClient(path=persist_directory)
        print(VECTOR_DB_INIT)

        if self.collection_exists(collection):
            print(f"{collection} found")
        else:            
            self.collection = self.chroma_client.get_or_create_collection(
                name="my_collection_complete",
                configuration={
                    "hnsw": {
                        "space": "cosine",
                        "ef_search": 100,
                        "ef_construction": 100,
                        "max_neighbors": 16,
                        "num_threads": 4
                    },
                    "embedding_function": None,
                    "dimensions": 1536
                }
            )
            print(VECTOR_COLLECTION_CREATED)

    def collection_exists(self, name:str)->bool:
        return any(c.name == name for c in self.chroma_client.list_collections())

    def save_frame_data(self, frameData:FrameData)->int:
        try:
            self.collection.add(
                ids=[frameData.id],
                embeddings=[frameData.embedding],
                metadatas=[{
                    "video_file":frameData.video_file,
                    "frame_file":frameData.frame_file,
                    "time_code":frameData.time_code,
                    "text":frameData.text,
                    "frame_type":frameData.frame_type
                }]
            )
            return 0
        except Exception as e:
          print(e)
          return 1
    
    def deleteCollection(self, collection_name):
        print(f"deleting {collection_name}")
        return self.chroma_client.delete_collection(name=collection_name)
    

   