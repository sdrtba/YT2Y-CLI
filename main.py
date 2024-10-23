from json import loads
import requests
import shutil
import yt_dlp


def upload(filename, target):
    with open(filename, "rb") as f:
        files = {"file": ("filename", f, "audio/mp3")}
        r = requests.post(url=target, files=files)
    return loads(r.text)


def get_target(filename):
    filename = ''.join(''.join(filename.split('\\')[1:]).split('.')[:-1])
    token = "" # put the yandex-music token
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://music.yandex.ru/handlers/ugc-upload.jsx?kind={kind}&filename={filename}" # kind=3 is a favourite`s id playlist

    print(filename)
    return loads(requests.get(url, headers=headers).text).get("post-target")


def progress_hook(d):
    if d['status'] == 'finished':
        print()

        filename = d['filename']
        target = get_target(filename)
        status = upload(filename, target)

        print(status)
        print("-----------------------------------------------")


def download():

    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s', # output template to name files as <title>.<ext>
        'paths': {'home': dir}, # temp and main files in one folder
        'format': 'ba[ext=m4a]', # bestaudio.m4a
        'retries': 5,
        'quiet': True, # without logs
        'progress': True, # show progress bar
        'skip_unavailable_fragments': True,
	    'noincludeunavailablevideos': True,
	    'ignoreerrors': True,
	    'no_warnings': True,
	    'playliststart': skip,

        'progress_hooks': [progress_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)
    except Exception as e:
        print(e)

    clear()


def clear():
    try:
        shutil.rmtree(dir)
    except:
        pass


if __name__ == '__main__':
    dir = 'output'
    clear()

    url = input('link (pass for https://www.youtube.com/playlist?list=PLcLWzrwuuZhNet5VdtPJBV-K0WDcRSvhJ): ')
    url = url if url != '' else "https://www.youtube.com/playlist?list=PLcLWzrwuuZhNet5VdtPJBV-K0WDcRSvhJ"

    kind = input('kind (pass for 3): ')
    kind = kind if kind != '' else 3

    skip = input('skip (pass for 0): ')
    skip = skip if skip != '' else 0

    download()
