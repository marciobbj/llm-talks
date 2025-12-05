import os
from openai import OpenAI

class LLMClient:
    def __init__(self, api_key: str, base_url: str, model: str, system_prompt: str):
        """
        Initialize the LLM Client.
        
        Args:
            api_key: API Key for the provider.
            base_url: Base URL for the API (e.g. https://openrouter.ai/api/v1 or http://localhost:11434/v1).
            model: Model name to use (e.g. google/gemini-2.0-flash-exp:free or llama3).
            system_prompt: The persona or system instruction for this specific client.
        """
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        self.model = model
        self.system_prompt = system_prompt
        self.history = [{"role": "system", "content": system_prompt}]

    def get_response(self, message: str) -> str:
        """
        Send a message to the LLM and get the response.
        Adds the user message to history and the assistant response to history.
        """
        self.history.append({"role": "user", "content": message})
        
        try:
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://llm-talks.local", # Optional for OpenRouter
                    "X-Title": "LLM Talks", # Optional for OpenRouter
                },
                model=self.model,
                messages=self.history,
            )
            response_content = completion.choices[0].message.content
            self.history.append({"role": "assistant", "content": response_content})
            return response_content
        except Exception as e:
            error_msg = f"Error communicating with {self.model}: {str(e)}"
            print(error_msg)
            return error_msg
