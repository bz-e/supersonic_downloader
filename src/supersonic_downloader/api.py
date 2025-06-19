from .supersonic_download import SupersonicDownloader
from typing import Optional


def coroutine_download(
    url: Optional[str] = None,
    job_nums: int = 200,
    file_path: Optional[str] = None,
    **kwargs,
) -> str:
    """
    Coroutine for downloading files from SupersonicDownloader
    """
    supersonic_download = SupersonicDownloader(url, job_nums, file_path, **kwargs)
    return supersonic_download.download(mode="coroutine")


def thread_download(
    url: Optional[str] = None,
    job_nums: int = 60,
    file_path: Optional[str] = None,
    **kwargs,
) -> str:
    """
    Thread for downloading files from SupersonicDownloader
    """
    supersonic_download = SupersonicDownloader(url, job_nums, file_path, **kwargs)
    return supersonic_download.download(mode="thread")
