import os
import cv2
import torch
import ffmpeg
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from openai import OpenAI
from dotenv import load_dotenv
import constants.constants
import shutil
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)

def extract_keyframes():
  print('keyframe extraction', constants.constants._VIDEO_FILE_IN)
  print(os.path.exists(constants.constants._VIDEO_FILE_IN))
  os.makedirs(constants.constants._OUTPUT_FOLDER, exist_ok=True)
  cap = cv2.VideoCapture(constants.constants._VIDEO_FILE_IN)
  if not cap.isOpened():
    raise IOError(f"failed to load {constants.constants._VIDEO_FILE_IN}")
  
  fps = cap.get(cv2.CAP_PROP_FPS)
  count = 0
  saved = 0
  while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      break
    if int(count % (fps * constants.constants.FRAMES_INTERVAL)) == 0:
      fname = os.path.join(constants.constants._OUTPUT_FOLDER, f"frame_{saved}.jpg")
      cv2.imwrite(fname, frame)
      saved += 1
    count += 1

  cap.release()

def embed_frames():
  model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
  processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
  embeddings = []
  for fname in sorted(os.listdir(constants.constants._OUTPUT_FOLDER)):
    if not fname.endswith(constants.constants._JPG):
      continue
    img_path = os.path.join(constants.constants._OUTPUT_FOLDER, fname)
    image = Image.open(img_path).convert(constants.constants._RGB)
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
      image_features = model.get_image_features(**inputs)
      embeddings.append((fname, image_features.numpy()))
      print(constants.constants._SEP)
      print(embeddings)
      print(constants.constants._SEP)
      print(constants.constants._EMBEDDING)
    return embeddings
  
def transfer_frames_to_s3():
    return 0
  
def clean_up_output_dir():
    shutil.rmtree(constants.constants._OUTPUT_FOLDER)
    print(constants.constants._CLEAN_UP)
    return 0

if __name__ == constants.constants._MAIN:
  extract_keyframes()
  embed_frames()
  clean_up_output_dir()
  transfer_frames_to_s3()