# YT-DL-SCLI 🐉

**yt-dl-scli (simple CLI)** is a script for downloading video in **MP4 format** and audio in **MP3 format** from youtube.com or other video platform using [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [FFmpeg](https://git.ffmpeg.org/ffmpeg.git).

- [INSTALLATION](#installation)
- [OPTIONS](#options)
- [EXAMPLES](#examples)

## INSTALLATION

To install it in **Termux** using [pipx](https://github.com/pypa/pipx), type:

```bash
$ pkg update
$ pkg upgrade
$ pkg install ffmpeg
$ pipx install "git+https://github.com/StipRabyn/yt-dl-scli/"
```

## OPTIONS

```
--help          Show help message and exit.
-a, --audio     Download audio in MP3 format.
-v, --video     Download video in MP4 format.
```

## EXAMPLES

Download audio from URL:

```bash
$ yt-dl-scli <URL> --audio
```

Download videos from a file with URLs:

```bash
$ yt-dl-scli $(cat urls.txt) --video
```

Secure audio download from a file with URLs **(Bash-script)**:

```bash
#!/bin/bash

if [ -z "$file" ]
then
  echo "Args?"
  exit 1
fi

for url in $(cat "$file")
do
  yt-dl-scli "$url" --audio
done < "$file"
```
