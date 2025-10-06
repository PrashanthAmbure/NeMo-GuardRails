from nemoguardrails.llm.providers import register_llm_provider
import httpx
from collections import namedtuple

async def serialize_prompt(prompt):
    if isinstance(prompt, list):
        # if it's a list of StringPromptValue objects
        return [p.text if hasattr(p, "text") else str(p) for p in prompt]
    else:
        # single StringPromptValue
        return prompt.text if hasattr(prompt, "text") else str(prompt)


class MyMicroserviceLLM:
    model_fields = {"model": True}
    def __init__(self, auth_url, chat_url, model="gpt", **kwargs):
        self.auth_url = auth_url
        self.chat_url = chat_url
        self.model = model
        # Store any extra kwargs as default_request_params
        self.default_request_params = dict(kwargs)  # <--- Add this line

    async def _acall(self, prompt, stop=None, **kwargs):
        async with httpx.AsyncClient() as client:
            # Step 1: Get Bearer token
            token_resp = await client.post(self.chat_url, json={...})  # Fill with your payload
            token = token_resp.json().get("access_token")

            # Step 2: Call chat completions
            headers = {"Authorization": f"Bearer {token}"}
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                # Add other params as needed
            }
            resp = await client.post(self.chat_url, headers=headers, json=payload)
            return resp.json()["choices"][0]["message"]["content"]

    async def agenerate_prompt(self, prompt, **kwargs):
        async with httpx.AsyncClient() as client:
            # payload = {"prompt": prompt.text}
            payload = {"prompt": await serialize_prompt(prompt)}
            response = await client.post(self.chat_url+'/chat', json=payload)
            Gen = namedtuple("Gen", ["text"])
            generations = [[Gen(text=response.text)]]
            LLMResult = namedtuple("LLMResult", ["llm_output", "generations"])
            return LLMResult(llm_output=response, generations=generations)
            # return response.text
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(self.chat_url+'/ping')
        #     print("Status code:", response.status_code)
        #     print("Response body:", response.text)
        # query_params = {**self.default_request_params, **kwargs}
        #
        # # Replace this set with your real auth payload!
        # auth_payload = {
        #     "username": "your_user",
        #     "password": "your_password"
        # }
        #
        # async with httpx.AsyncClient() as client:
        #     token_resp = await client.post(self.auth_url, json=auth_payload)
        #     token = token_resp.json().get("access_token")
        #
        #     headers = {"Authorization": f"Bearer {token}"}
        #     payload = {
        #         "model": self.model,
        #         "messages": [{"role": "user", "content": await serialize_prompt(prompt)}],
        #         "temperature": query_params.get("temperature", 1.0),
        #         # Add other supported parameters here (“top_p”, etc)
        #     }
        #     resp = await client.post(self.chat_url, headers=headers, json=payload)
        #     from types import SimpleNamespace
        #     from collections import namedtuple
        #
        #     data = resp.json()
        #     text = data["choices"][0]["message"]["content"]
        #
        #     Gen = namedtuple("Gen", ["text"])
        #     generations = [[Gen(text=text)]]
        #
        #     LLMResult = namedtuple("LLMResult", ["llm_output", "generations"])
        #     return LLMResult(llm_output=data, generations=generations)
            # return resp.json()["choices"][0]["message"]["content"]



register_llm_provider("microservice_llm", MyMicroserviceLLM)
