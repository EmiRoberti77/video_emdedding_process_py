"""Constants used across the application."""

import os
from dotenv import load_dotenv
load_dotenv()



EMPTY = ""
SEP = '_______________________________'
JPG = '.jpg'
RGB = 'RGB'
MAIN = '__main__'
PROCESS_COMPLETED = 'process_completed'
EMBEDDING = "Embedding " + PROCESS_COMPLETED
CLEAN_UP = "Clean up " + PROCESS_COMPLETED
VIDEO_FILE_IN = './video/sample.mp4'
AUDIO_FILE_IN = './audio/sample.mp3'
OUTPUT_FOLDER = 'output'
FRAMES_INTERVAL = 5
VECTOR_COLLECTION_NAME = "audio_video_vectors"
VECTOR_STORE = "./chroma_store"
VECTOR_DB_INIT = 'initialized vector db'
VECTOR_COLLECTION_CREATED = 'vector collection created'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
