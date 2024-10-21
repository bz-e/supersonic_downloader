# supersonic_downloader
**A multi-threaded, multi-coroutine download tool written in Python.When you need to download some relatively large model parameters, you can use this package directly in the Python code to quickly download the model parameters, and it supports proxies.**

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
# Cloning the repository
```shell
git clone https://github.com/bz-e/supersonic_downloader.git


