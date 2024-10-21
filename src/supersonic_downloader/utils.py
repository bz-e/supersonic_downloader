# import subprocess
# import os


# def run_git_command(repo_path, command):
#     """Run a git command and return the output."""
#     os.chdir(repo_path)

#     result = subprocess.run(
#         command,
#         shell=True,
#         capture_output=True,
#         text=True,
#     )
#     return (result.stdout).strip()
#     # git clone https://hf-mirror.com/nvidia/Llama-3.1-Nemotron-70B-Instruct-HF
