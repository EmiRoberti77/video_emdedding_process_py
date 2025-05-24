from sample_text import SAMPLE_AUDIO_TRANSCRIPT
import re

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
    #split audio text into 200 words chunks
    #print(words)
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, word_count, chunk_size)]
    print(len(chunks))
    [print(f"[", chunk, "]") for chunk in chunks]


chunk_text(SAMPLE_AUDIO_TRANSCRIPT)


