import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.supersonic_downloader import thread_download, coroutine_download, STATE_MESSAGE

# from src.supersonic_downloader.utils import run_git_command


params1 = pytest.mark.parametrize(
    "url,proxy,expected",
    [
        (
            "https://hf-mirror.com/google-bert/bert-base-cased/resolve/main/flax_model.msgpack?download=true",
            {"http": "http://127.0.0.1:8080"},
            STATE_MESSAGE,
        )
    ],
)


params2 = pytest.mark.parametrize(
    "url,file_path,proxy,expected",
    [
        (
            "https://hf-mirror.com/google-bert/bert-base-cased/resolve/main/tf_model.h5?download=true",
            "download_file/model.safetensors",
            {"http": "http://127.0.0.1:8080"},
            STATE_MESSAGE,
        )
    ],
)


params3 = pytest.mark.parametrize(
    "url,file_path,expected",
    [
        (
            "https://hf-mirror.com/google-bert/bert-base-cased/resolve/main/tf_model.h5?download=true",
            "download_file/model.safetensors",
            STATE_MESSAGE,
        )
    ],
)


params4 = pytest.mark.parametrize(
    "url,expected",
    [
        (
            "https://hf-mirror.com/google-bert/bert-base-cased/resolve/main/flax_model.msgpack?download=true",
            STATE_MESSAGE,
        )
    ],
)


# @params1
# def test_thread_download(url, proxy, expected):
#     assert thread_download(url=url, proxy=proxy) == expected


@params4
def test_thread_download2(url, expected):
    assert thread_download(url=url) == expected


# @params2
# def test_coroutine_download(url, file_path, proxy, expected):
#     assert coroutine_download(url=url, file_path=file_path, proxy=proxy) == expected


@params3
def test_coroutine_download2(url, file_path, expected):
    assert coroutine_download(url=url, file_path=file_path) == expected


# @pytest.mark.parametrize(
#     "repo_path,command,expected",
#     [
#         (
#             "/Users/evan.zhang5/workspace/pythonProject/HF-Model-Mulit-Process-Download/HF-MP-Model-Download/download_file",
#             "git --version",
#             "git version 2.39.3 (Apple Git-146)",
#         )
#     ],
# )
# def test_git(repo_path, command, expected):
#     assert run_git_command(repo_path, command) == expected
