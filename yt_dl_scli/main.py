import os
import subprocess
import click
from yt_dlp import YoutubeDL


def downloadFilesGetFileNames(urls: tuple[str],
                              options: dict[str, bool]) -> list[str]:
    """
    Download files from URLs and return file names.

    :param urls:     Video URLs.
    :param options:  Options for YoutubeDL class.
    :return:         List of filenames.
    """
    with YoutubeDL(options) as ydl:
        urlsInfo = [ydl.extract_info(url) for url in urls]
        filenames = [ydl.prepare_filename(info) for info in urlsInfo]
        ydl.download(urls)

    return filenames


def processRun(filename: str, command: str) -> None:
    """
    Create a file with a new format using FFmpeg.

    :param filename:  File name with an old format.
    :param command:   Command to call FFmpeg.
    """
    if os.path.exists(filename):
        subprocess.run(command, shell=True)
        os.remove(filename)  # Remove a file with an old format.
    else:
        click.echo(f'[{__name__}] No such file: "{filename}"!')


@click.command(help="""
Script for downloading video and audio 
from youtube.com or other video platform.
""")
@click.argument("urls", nargs=-1, required=True)  # Unlimited number of args.
@click.option("-a", "--audio", is_flag=True, help="Download audio in MP3 format.")
@click.option("-v", "--video", is_flag=True, help="Download video in MP4 format.")
def run(urls: tuple[str], audio: str, video: str) -> None:
    """
    Click command-line tool.

    :param urls:   Video URLs.
    :param audio:  Download audio in MP3 format.
    :param video:  Download video in MP4 format.
    """
    options = {"outtmpl": "%(title)s.%(ext)s"}  # Options for downloading video.

    if video:
        # Download WEBM files and get file names.
        filenames = downloadFilesGetFileNames(urls, options)
        # WEBM to MP4.
        for f in filenames:
            processRun(f, f'ffmpeg -i "{f}" -c:v copy "{f[:-5]}.mp4"')

    if audio:
        # Add options for downloading audios.
        options.update(
            {
                "format": "m4a/bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "m4a",
                    }
                ],
            }
        )
        # Download M4A files and get file names.
        filenames = downloadFilesGetFileNames(urls, options)
        # M4A to MP3.
        for f in filenames:
            processRun(
                f, f'ffmpeg -i "{f}" -c:v copy -c:a libmp3lame -q:a 4 "{f[:-4]}.mp3"'
            )
