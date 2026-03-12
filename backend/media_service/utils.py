def extend_url(url: str, path: str) -> str:
    return url.rstrip("/") + path

def prints(info):
    print(f"[MEDIA_SERVICE]:    {info}")