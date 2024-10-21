from .supersonic_download import SupersonicDownloader


def coroutine_download(url: str = None, job_nums=200, file_path=None, **kwargs):
    """
    Coroutine for downloading files from SupersonicDownloader
    """
    supersonic_download = SupersonicDownloader(url, job_nums, file_path, **kwargs)
    return supersonic_download.download(mode="coroutine")


def thread_download(url: str = None, job_nums=60, file_path=None, **kwargs):
    """
    Thread for downloading files from SupersonicDownloader
    """
    supersonic_download = SupersonicDownloader(url, job_nums, file_path, **kwargs)
    return supersonic_download.download(mode="thread")
