# sample video

```bash
pip install -U yt-dlp
```

## video decode from youtube to mp4

download the file

```bash
yt-dlp -o "video/news_sample.mp4" "https://www.youtube.com/watch?v=-tQja40T8Tg"
```

force mp4

```bash
yt-dlp -f 'bv*+ba/b[ext=mp4]' --merge-output-format mp4 -o "video/news_sample.mp4" "https://www.youtube.com/watch?v=-tQja40T8Tg"
```

force mp4 + best audio

```bash
yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 -o "video/news_sample.mp4" "https://www.youtube.com/watch?v=-tQja40T8Tg"
```

```bash
yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 -o "video/news_sample.mp4" "https://www.youtube.com/watch?v=WxUN9jWr6H8"
```

if needed and the file comes down as a .webm format then use ffmpeg to transcode to mp4

```bash
ffmpeg -i ./video/news_sample.mp4.webm -c:v libx264 -c:a aac ./video/news_sample.mp4
```

## audio decode from youtube to mp3

```bash
yt-dlp -x --audio-format mp3 "https://www.youtube.com/watch?v=-tQja40T8Tg"
```
