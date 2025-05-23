"""Main module for extracting and embedding keyframes."""

import os
import shutil
import re
from typing import List
import uuid
import cv2
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from constants import constants
from vector_db.collection_manager import CollectionManager as CM, FrameData
import whisper
from openai import OpenAI


_DEBUG = False
print(constants.OPENAI_API_KEY)
model = OpenAI(api_key=constants.OPENAI_API_KEY)

cm = CM(constants.VECTOR_STORE, constants.VECTOR_COLLECTION_NAME)

def extract_keyframes()->List[str]:
    """Extract keyframes from video at fixed intervals."""
    print('keyframe extraction', constants.VIDEO_FILE_IN)
    frameList = []
    print(os.path.exists(constants.VIDEO_FILE_IN))
    os.makedirs(constants.OUTPUT_FOLDER, exist_ok=True)
    cap = cv2.VideoCapture(constants.VIDEO_FILE_IN)
    if not cap.isOpened():
        raise IOError(f"failed to load {constants.VIDEO_FILE_IN}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    saved = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if int(count % (fps * constants.FRAMES_INTERVAL)) == 0:
            fname = os.path.join(constants.OUTPUT_FOLDER, f"frame_{saved}.jpg")
            cv2.imwrite(fname, frame)
            saved += 1
            frameList.append(fname)
        count += 1

    cap.release()
    return frameList


def embed_frames():
    """Embed extracted frames using CLIP."""
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    embeddings = []
    for fname in sorted(os.listdir(constants.OUTPUT_FOLDER)):
        if not fname.endswith(constants.JPG):
            continue
        img_path = os.path.join(constants.OUTPUT_FOLDER, fname)
        image = Image.open(img_path).convert(constants.RGB)
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            image_features = model.get_image_features(**inputs)
            embeddings.append((fname, image_features.numpy()))
            print(constants.SEP)
            print(embeddings)
            print(constants.SEP)
            print(constants.EMBEDDING)
    return embeddings

def chunk_text(text, chunk_size=200):
    """
        Function to break large text that has come from audio transcoding.
        When looking to turn text into embeddings, best to keep to about 
        512, 1024 tokens. About 200 words.
    """
    text_len = len(text)
    words = re.findall(r'\b\w+\b', text)
    word_count = len(words)
    print('text len', text_len)
    print('word count', word_count)
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, word_count, chunk_size)]
    return chunks


def embed_text(text):
    """Function to embed text, this text has been extracted from the audio track"""
    response = model.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def transfer_frames_to_s3():
    """Placeholder for uploading frames to S3"""
    return 0

def transcribe_audio(model):
    """transcribe audio to text using whisper"""
    model = whisper.load_model(model)
    result = model.transcribe(constants.AUDIO_FILE_IN)
    return result["text"]

def clean_up_output_dir():
    """Remove output directory and log clean-up."""
    shutil.rmtree(constants.OUTPUT_FOLDER)
    print(constants.CLEAN_UP)
    return 0

def save_embedding_to_database(text, embedding, video_file, frame_file, time_code):
    print(len(text))
    print(len(embedding))
    frameData = FrameData(
        id=str(uuid.uuid4()),
        text=text,
        embedding=embedding,
        video_file=video_file,
        frame_file=frame_file,
        time_code=time_code,
        frame_type='image'
    )
    ret = cm.save_frame_data(frameData=frameData)
    print('saving to database', ret)
    return 0


if __name__ == constants.MAIN:
    del_col = input(">delete collection y/n?")
    if del_col == "y":
        ret = cm.deleteCollection(constants.VECTOR_COLLECTION_NAME)
        print(ret)
    else:    
        video = input('>video y/n?')
        print(f"video:{video}")
        audio = input('>audio y/n?')
        print(f"audio:{audio}")
        frameList = extract_keyframes()
        if video == 'y':        
            embed_frames()

        if audio == 'y':
            
            audio_text = transcribe_audio('tiny')
            speech_chunks = chunk_text(audio_text)
            if _DEBUG ==  True:
                [print(F"[{chunk}]") for chunk in speech_chunks]

            [save_embedding_to_database(chunk, embed_text(chunk), constants.VIDEO_FILE_IN, frameList[0], 0) for chunk in speech_chunks]

            #audio_embedding = embed_text(audio_text)
            #print(audio_text)
            #print(audio_embedding)
        
        ##clean_up_output_dir()
        transfer_frames_to_s3()