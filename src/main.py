import os
import cv2
from dotenv import load_dotenv
load_dotenv()

VIDEO_FILE_IN = './video/sample.mp4'
OUTPUT_FOLDER = 'output'
FRAMES_INTERVAL = 5
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)

def extract_keyframes():
  print('keyframe extraction', VIDEO_FILE_IN)
  print(os.path.exists(VIDEO_FILE_IN))
  os.makedirs(OUTPUT_FOLDER, exist_ok=True)
  cap = cv2.VideoCapture(VIDEO_FILE_IN)
  if not cap.isOpened():
    raise IOError(f"failed to load {VIDEO_FILE_IN}")
  
  fps = cap.get(cv2.CAP_PROP_FPS)
  count = 0
  saved = 0
  while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      break
    if int(count % (fps * FRAMES_INTERVAL)) == 0:
      fname = os.path.join(OUTPUT_FOLDER, f"frame_{saved}.jpg")
      cv2.imwrite(fname, frame)
      saved += 1
    count += 1

  cap.release()

if __name__ == "__main__":
  extract_keyframes()