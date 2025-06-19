import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger
import time
import uuid
import asyncio
import aiohttp
import inspect
from typing import Optional

STATE_MESSAGE = "Download Success!"


class SupersonicDownloader:
    """Supersonic Downloader Class"""

    def __init__(
        self,
        url: Optional[str] = None,
        job_nums: int = 30,
        file_path: Optional[str] = None,
        retries: int = 10,
        **kwargs,
    ) -> None:
        """
        Intitialize the Supersonic Downloader.
        :param url: URL of the file to download.
        :param job_nums: Number of concurrent download jobs.
        :file_path: Path to save the downloaded file.
        :retries: Number of retries for each download job.
        :kwargs: (optional) additional keyword arguments.
        :hooks: (optional) list of hooks to be called after each download job.
        :chunk_size: (optional) size of each chunk to download.
        :proxy: (optional) proxy to use for the download.
        :return: None
        """
        if not url:
            logger.error("url cannot be none")
            return
        self.url = url
        self.job_nums = job_nums
        self.session = requests.Session()
        self.proxy = None
        if "hooks" in kwargs:
            assert isinstance(kwargs["hooks"], list)
            self.session.hooks["response"] = kwargs["hooks"]

        if "proxy" in kwargs:
            assert isinstance(kwargs["proxy"], dict)
            self.session.proxies = kwargs["proxy"]
            self.proxy = kwargs["proxy"]["http"]

        res = self.session.head(self.url, timeout=30)
        self.retries = retries

        # redirect
        redirct_start_time = time.time()
        while res.status_code in (301, 302):
            self.url = res.headers["Location"]
            res = self.session.head(self.url, timeout=30)
            redirct_middle_time = time.time()
            if (redirct_middle_time - redirct_start_time) > 60:
                logger.error("redirct timeout!")
                break
        if res.status_code != 200:
            logger.error(f"download error, status code:{res.status_code}")
            return

        # get file size
        self.file_size = int(res.headers["Content-Length"])
        # get file path
        self.file_path = str(uuid.uuid4().hex) if not file_path else file_path

        # get  positions for each download job
        positions = []
        slice_size = self.file_size // self.job_nums
        for i in range(self.job_nums):
            start_pos = i * slice_size
            end_pos = (i + 1) * slice_size - 1
            if i == self.job_nums - 1:
                end_pos = self.file_size - 1
            positions.append((start_pos, end_pos))
        self.positions = positions

    def _thread_downloadTask(self, start_pos: int, end_pos: int, chunk_size: int):
        """Download a specific range of the file using thread.

        :param start_pos: Start position of the range to download.
        :param end_pos: End position of the range to download.
        :param chunk_size: Size of each chunk to download.
        :return: None
        """
        for count in range(self.retries):
            try:
                headers = {"Range": f"bytes={start_pos}-{end_pos}"}
                res = self.session.get(url=self.url, headers=headers, stream=True)
                with open(self.file_path, "rb+") as f:
                    f.seek(start_pos)
                    for chunk in res.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                return
            except Exception as e:
                logger.error(f"request _downloadTask  error:{e}")
                time.sleep(1)
                if count == self.retries - 1:
                    logger.error("_downloadTask error, retry failed")
                    raise Exception(
                        f"{inspect.currentframe().f_code.co_name} : _downloadTask error, retry failed"
                    )

    def _thread_download(self, chunk_size: int = 256 * 1024):
        """Download the file using thread.

        :param chunk_size: Size of each chunk to download.
        :return: None
        """
        with ThreadPoolExecutor(max_workers=self.job_nums + 1) as pool:
            futures = []
            for start_pos, end_pos in self.positions:
                futures.append(
                    pool.submit(
                        self._thread_downloadTask, start_pos, end_pos, chunk_size
                    )
                )
            # wait for all tasks to complete
            as_completed(futures)

    async def _coroutine_downloadTask(self, session, start_pos, end_pos):
        """Download a specific range of the file using coroutine.

        :param session: aiohttp.ClientSession object.
        :param start_pos: Start position of the range to download.
        :param end_pos: End position of the range to download.
        :return: None
        """

        for count in range(self.retries):
            try:
                headers = {"Range": f"bytes={start_pos}-{end_pos}"}
                async with session.get(
                    url=self.url, headers=headers, proxy=self.proxy
                ) as res:
                    with open(self.file_path, "rb+") as f:
                        f.seek(start_pos)
                        async for chunk, _ in res.content.iter_chunks():
                            if chunk:
                                f.write(chunk)

                return
            except Exception as e:
                logger.error(f"request _downloadTask  error:{e}")
                if count == self.retries - 1:
                    logger.error("_downloadTask error, retry failed")
                    raise Exception(
                        f"{inspect.currentframe().f_code.co_name} : _downloadTask error, retry failed"
                    )

    async def _coroutine_download(self):
        tasks = []
        connector = None
        trust_env = False
        if self.proxy:
            connector = aiohttp.TCPConnector(ssl=False)
            trust_env = True
        timeout = aiohttp.ClientTimeout(total=60 * 60, sock_read=240)
        async with aiohttp.ClientSession(
            connector=connector, trust_env=trust_env, timeout=timeout
        ) as session:
            for start_pos, end_pos in self.positions:
                tasks.append(self._coroutine_downloadTask(session, start_pos, end_pos))
            await asyncio.gather(*tasks)

    def download(self, mode: str = "thread", chunk_size: int = 256 * 1024) -> str:
        """Download the file.

        :param mode: Download mode, "thread" or "coroutine".
        :param chunk_size: Size of each chunk to download.
        """

        with open(self.file_path, "wb+") as f:
            pass
        start_time = time.time()
        if mode == "thread":
            self._thread_download(chunk_size=chunk_size)
        elif mode == "coroutine":
            asyncio.run(self._coroutine_download())
        else:
            logger.error("mode error")
            return
        end_time = time.time()
        logger.info(
            f"download success, file size:{self.file_size} bytes ,cost time:{end_time - start_time:.2f} s"
        )
        return STATE_MESSAGE
