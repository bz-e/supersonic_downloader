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
# usage
```python
from supersonic_downloader import thread_download, coroutine_download

url = "https://hf-mirror.com/google-bert/bert-base-cased/resolve/main/flax_model.msgpack?download=true"
file_path = "download_file/model.safetensors"
proxy={"http": "http://127.0.0.1:8080","https": "http://127.0.0.1:8080"} # [optional]
hooks=[lambda x :print(f"print response statue code:{x.status_code}")] # [optional] after response, you can do something

```


# Cloning the repository
```shell
git clone https://github.com/bz-e/supersonic_downloader.git
```


