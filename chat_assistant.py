from typing import List, Union
import re
import requests
import logging
import time
import curlify
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VllmChat:
    def __init__(
        self, server_ip, server_port, model_name_or_path="Ling-2.5-1T", api_key=None, schema="http"
    ):
        self.model_name_or_path = model_name_or_path
        self.generation_config = dict(
            temperature=0.001,
            top_p=0.5,
            repetition_penalty=None,
            top_k=None,
            stop=None,
            max_tokens=None,
        )
        self.url = f"{schema}://{server_ip}:{server_port}/v1/chat/completions"
        self.api_key = api_key
        print(f"valid url: {self._filter_valid_urls([self.url])}")

    def _filter_valid_urls(self, urls: List[str]) -> List[str]:
        """仅保留能连接且模型 ID 匹配的 URL"""
        url_base_re = re.compile(r"(https?://[\.:\w]+?)/v1/chat/completions")
        headers = {"Content-Type": "application/json"}
        if self.api_key is not None:
            headers["Authorization"] = f"Bearer {self.api_key}"
        valid = []
        for url in urls:
            m = url_base_re.match(url)
            if not m:
                continue
            try:
                resp = requests.get(
                    f"{m.group(1)}/v1/models", timeout=1, headers=headers
                )
                # print(f"{resp.json()}")
                if resp.status_code == 200 and self.model_name_or_path in [
                    model_card.get("id", "")
                    for model_card in resp.json().get("data", [{}])
                ]:
                    valid.append(url)
            except requests.RequestException:
                pass
            finally:
                if "resp" in locals() and resp is not None:
                    resp.close()
        return valid

    def pre_process(self, query):
        return query

    def post_process(self, response):
        return response

    def set_generation_config(
        self,
        temperature=None,
        top_p=None,
        repetition_penalty=None,
        top_k=None,
        stop=None,
        max_tokens=None,
    ):
        if temperature is not None:
            self.generation_config["temperature"] = temperature
        if top_p is not None:
            self.generation_config["top_p"] = top_p
        if repetition_penalty is not None:
            self.generation_config["repetition_penalty"] = repetition_penalty
        if top_k is not None:
            self.generation_config["top_k"] = top_k
        if stop is not None:
            self.generation_config["stop"] = stop
        if max_tokens is not None:
            self.generation_config["max_tokens"] = max_tokens

    def chat(
        self, query, history, n=1, system_prompt="You are a helpful assistant.", retry=10000
    ) -> Union[str, List[str]]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        for _query, _response in history:
            messages.append({"role": "user", "content": _query})
            messages.append({"role": "assistant", "content": _response})
        messages.append({"role": "user", "content": query})

        payload = {
            "model": self.model_name_or_path,
            "messages": messages,
            "temperature": self.generation_config["temperature"],
            "top_p": self.generation_config["top_p"],
        }
        if n != 1:
            payload["n"] = n
        if self.generation_config["top_k"] is not None:
            payload["top_k"] = self.generation_config["top_k"]
        if self.generation_config["repetition_penalty"] is not None:
            payload["repetition_penalty"] = self.generation_config["repetition_penalty"]
        if self.generation_config["stop"] is not None:
            payload["stop"] = self.generation_config["stop"]

        headers = {"Content-Type": "application/json"}
        if self.api_key is not None:
            headers["Authorization"] = f"Bearer {self.api_key}"

        last_exception = None
        response = None

        for attempt in range(retry):
            try:
                response = requests.post(self.url, json=payload, headers=headers)
                curl_command = curlify.to_curl(response.request)
                logger.debug(curl_command)

                if response.status_code == 200:
                    contents = [
                        choice["message"]["content"]
                        for choice in response.json().get("choices")
                    ]
                    return contents
                else:
                    logger.warning(
                        f"Attempt {attempt + 1} failed with status code: {response.status_code}"
                    )
                    last_exception = Exception(f"HTTP {response.status_code}")
                    response.close()
                    response = None

            except requests.RequestException as e:
                logger.warning(
                    f"Attempt {attempt + 1} failed with {type(e).__name__}: {str(e)}"
                )
                last_exception = e
                if response:
                    response.close()
                    response = None

            except Exception as e:
                logger.error(
                    f"Attempt {attempt + 1} failed with unexpected {type(e).__name__}: {str(e)}"
                )
                last_exception = e
                if response:
                    response.close()
                    response = None

            # If not the last attempt, wait before retrying
            if attempt < retry - 1:
                sleep_time = min(
                    2**attempt, 10
                )  # Exponential backoff with max 10 seconds
                logger.info(f"Waiting {sleep_time} seconds before retry...")
                time.sleep(sleep_time)

        # All retries failed
        if last_exception:
            logger.error(
                f"All {retry} attempts failed. Last error: {str(last_exception)}"
            )
        else:
            logger.error(f"All {retry} attempts failed with unknown error")

        return None
    
    def chat_messages(
        self, messages, n=1, retry=100
    ) -> Union[str, List[str]]:
        payload = {
            "model": self.model_name_or_path,
            "messages": messages,
            "temperature": self.generation_config["temperature"],
            "top_p": self.generation_config["top_p"],
        }
        if n != 1:
            payload["n"] = n
        if self.generation_config["top_k"] is not None:
            payload["top_k"] = self.generation_config["top_k"]
        if self.generation_config["repetition_penalty"] is not None:
            payload["repetition_penalty"] = self.generation_config["repetition_penalty"]
        if self.generation_config["stop"] is not None:
            payload["stop"] = self.generation_config["stop"]

        headers = {"Content-Type": "application/json"}
        if self.api_key is not None:
            headers["Authorization"] = f"Bearer {self.api_key}"

        last_exception = None
        response = None

        for attempt in range(retry):
            try:
                response = requests.post(self.url, json=payload, headers=headers)
                curl_command = curlify.to_curl(response.request)
                # logger.debug(curl_command)

                if response.status_code == 200:
                    contents = [
                        choice["message"]["content"]
                        for choice in response.json().get("choices")
                    ]
                    return contents
                else:
                    # logger.warning(
                    #     f"Attempt {attempt + 1} failed with status code: {response.status_code}"
                    # )
                    last_exception = Exception(f"HTTP {response.status_code}")
                    response.close()
                    response = None

            except requests.RequestException as e:
                # logger.warning(
                #     f"Attempt {attempt + 1} failed with {type(e).__name__}: {str(e)}"
                # )
                last_exception = e
                if response:
                    response.close()
                    response = None

            except Exception as e:
                # logger.error(
                #     f"Attempt {attempt + 1} failed with unexpected {type(e).__name__}: {str(e)}"
                # )
                last_exception = e
                if response:
                    response.close()
                    response = None

            # If not the last attempt, wait before retrying
            if attempt < retry - 1:
                sleep_time = random.randint(5, 60)  # Exponential backoff with max 10 seconds
                # logger.info(f"Waiting {sleep_time} seconds before retry...")
                time.sleep(sleep_time)

        # All retries failed
        # if last_exception:
        #     logger.error(
        #         f"All {retry} attempts failed. Last error: {str(last_exception)}"
        #     )
        # else:
        #     logger.error(f"All {retry} attempts failed with unknown error")

        return None



def init_client(model_name_or_path):

    chat_client = VllmChat(schema="https", server_ip="antchat.alipay.com", server_port="443",
                           api_key="jYv5dM5jLZckPUF4Amg8V40h3ywZcmVL", model_name_or_path=model_name_or_path)
    chat_client.set_generation_config(
        temperature=1.0, top_p=1.0, max_tokens=16384
    )
    return chat_client