import os
import shutil
import hmac
import hashlib
import base64
import subprocess
import time
from mysite.logger import logger
import async_timeout
import asyncio
import mysite.interpreter.interpreter_config 
from models.ride import test_set_lide
from mysite.libs.github import github
GENERATION_TIMEOUT_SEC=60
BASE_PATH = "/home/user/app/controllers/"

def set_environment_variables():
    os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
    os.environ["OPENAI_API_KEY"] = "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"
    os.environ["MODEL_NAME"] = "llama3-8b-8192"
    os.environ["LOCAL_MODEL"] = "true"

def validate_signature(body: str, signature: str, secret: str) -> bool:
    if secret is None:
        logger.error("Secret is None")
        return False

    hash = hmac.new(
        secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256
    ).digest()
    expected_signature = base64.b64encode(hash).decode("utf-8")
    return hmac.compare_digest(expected_signature, signature)

def no_process_file(prompt, foldername):
    set_environment_variables()
    try:
        proc = subprocess.Popen(["mkdir", f"{BASE_PATH}{foldername}"])
    except subprocess.CalledProcessError as e:
        return f"Processed Content:\n{e.stdout}\n\nMake Command Error:\n{e.stderr}"

    no_extension_path = f"{BASE_PATH}{foldername}/prompt"
    time.sleep(1)
    with open(no_extension_path, "a") as f:
        f.write(prompt)
    time.sleep(1)
    try:
        prompt_file_path = no_extension_path
        with open(prompt_file_path, "a") as prompt_file:
            prompt_file.write(prompt)
    except Exception as e:
        return f"Error writing prompt to file: {str(e)}"
    time.sleep(1)

    try:
        proc = subprocess.Popen(
            ["make", "run", foldername],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = proc.communicate(input="n\ny\ny\n")
        return f"Processed Content:\n{stdout}\n\nMake Command Output:\n{stdout}\n\nMake Command Error:\n{stderr}"
    except subprocess.CalledProcessError as e:
        return f"Processed Content:\n{e.stdout}\n\nMake Command Error:\n{e.stderr}"



def process_file(fileobj, prompt, foldername,token=None):
    set_environment_variables()
    try:
        proc = subprocess.Popen(["mkdir", f"{BASE_PATH}{foldername}"])
    except subprocess.CalledProcessError as e:
        return f"Processed Content:\n{e.stdout}\n\nMake Command Error:\n{e.stderr}"
    time.sleep(2)
    path = f"{BASE_PATH}{foldername}/" + os.path.basename(fileobj)
    shutil.copyfile(fileobj.name, path)
    base_name = os.path.splitext(os.path.basename(fileobj))[0]
    no_extension_path = f"{BASE_PATH}{foldername}/{base_name}"
    shutil.copyfile(fileobj, no_extension_path)
    with open(no_extension_path, "a") as f:
        f.write(prompt)
    try:
        prompt_file_path = no_extension_path
        with open(prompt_file_path, "w") as prompt_file:
            prompt_file.write(prompt)
    except Exception as e:
        return f"Error writing prompt to file: {str(e)}"
    time.sleep(1)
    #foldernameの登録
    test_set_lide(prompt,foldername)
    try:
        proc = subprocess.Popen(
            ["make", "run", foldername],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = proc.communicate(input="n\ny\ny\n")
        url = github(token)
        return f"Processed {url} Content:\n{stdout}\n\nMake Command Output:\n{stdout}\n\nMake {url} Command Errore:\n{stderr}"
    except subprocess.CalledProcessError as e:
        return f"Processed Content:\n{stdout}\n\nMake Command  {url} Errore:\n{e.stderr}"

