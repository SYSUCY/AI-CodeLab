import sys
import os
import requests

CODE_RUNNER_IP = os.environ.get("AI_CODELAB_CODE_RUNNER_IP")
if CODE_RUNNER_IP is None:
    raise ValueError("Environment variable AI_CODELAB_CODE_RUNNER_IP is not set")

POST_URL = f"http://{CODE_RUNNER_IP}:8000/run_code/"


def run_code(language, code):
    data = {"language": language, "code": code}

    response = requests.post(POST_URL, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

    # if language not in language_map:
    #     raise ValueError(f"Language {language} is not supported")
