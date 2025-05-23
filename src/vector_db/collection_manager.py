import dataclasses
import chromadb
from typing import List
from constants.constants import VECTOR_DB_INIT, VECTOR_COLLECTION_CREATED

@dataclasses
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
        self.chroma_client = chromadb.Client(chromadb.config.Settings(
            persist_directory=persist_directory
        ))
        print(VECTOR_DB_INIT)

        collection = self.chroma_client.get_or_create_collection(name=collection)
        print(VECTOR_COLLECTION_CREATED)

    def save_frame_data(self, frameData:FrameData)->int:
        self.collection.add(
            ids=[frameData.id],
            embedding=[frameData.embedding],
            metadata=[{
                "video_file":frameData.video_file,
                "frame_file":frameData.frame_file,
                "time_code":frameData.time_code,
                "text":frameData.text,
                "frame_type":frameData.frame_type
            }]
        )

    

   