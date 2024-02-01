from pytube import Playlist, YouTube
from json import loads
import requests
import os


def download(video: YouTube) -> str:
    stream = video.streams.filter(adaptive=True, only_audio=True)[-1]
    file = stream.download().split('\\')[-1].split('.')
    return '.'.join(file)


def get_target(filename: str) -> str:
    token = "y0_AgAAAABhcb3WAAG8XgAAAADg8YLp8YmhqzOQTT6adR-8RdZ-NriSgXc"
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://music.yandex.ru/handlers/ugc-upload.jsx?kind=3&filename={''.join(filename.split('.')[:-1])}"
    return loads(requests.get(url, headers=headers).text).get("post-target")


def upload(filename: str, target: str) -> dict:
    with open(filename, "rb") as f:
        files = {"file": ("filename", f, "audio/mp3")}
        r = requests.post(url=target, files=files)
    os.remove(filename)
    return loads(r.text)


def main(url: str = "https://www.youtube.com/playlist?list=PLcLWzrwuuZhNet5VdtPJBV-K0WDcRSvhJ"):
    p = Playlist(url)
    for video in p.videos:
        filename = download(video)
        target = get_target(filename)
        status = upload(filename, target)
        print(filename)
        print(status)
        print("-----------------------------------------------")


if __name__ == "__main__":
    url = input("url: ")
    main()
