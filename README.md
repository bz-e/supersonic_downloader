# supersonic_downloader
**A multi-threaded, multi-coroutine download tool written in Python.When you need to download some relatively large model parameters ，videos or other large files, you can use this package directly in the Python code to quickly download what you need, and it supports proxies.**
**一个用python编写的多线程、多协程下载器，可以帮助你在深度学习代码里高速下载模型参数，也能帮你下快速载长视频、大文件**

# Quick Start
```python
from supersonic_downloader import thread_download, coroutine_download

url = "https://hf-mirror.com/google-bert/bert-base-cased/resolve/main/flax_model.msgpack?download=true"
file_path = "download_file/model.safetensors"

thread_download(url=url, file_path=file_path) # multi-threaded download
coroutine_download(url=url, file_path=file_path) # multi-coroutine download
```

# Installing
```shell
pip install supersonic_downloader
```
# Usage
```python
from supersonic_downloader import thread_download, coroutine_download

url = "https://hf-mirror.com/google-bert/bert-base-cased/resolve/main/flax_model.msgpack?download=true"
file_path = "download_file/model.safetensors"
proxy={"http": "http://127.0.0.1:8080","https": "http://127.0.0.1:8080"} # [optional]
hooks=[lambda x :print(f"print response statue code:{x.status_code}")] # [optional] after response, you can do something

thread_download(url=url, file_path=file_path, proxy=proxy, hooks=hooks) # multi-threaded download
coroutine_download(url=url, file_path=file_path, proxy=proxy, hooks=hooks) # multi-coroutine download

```


# Cloning the repository
```shell
git clone https://github.com/bz-e/supersonic_downloader.git
```


