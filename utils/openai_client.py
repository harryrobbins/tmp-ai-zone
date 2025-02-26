import requests
import json
import os


class OpenAIClient:
    """Client for interacting with OpenAI API"""

    def __init__(self, api_key=None, api_url=None):
        """Initialize the OpenAI client with API credentials"""
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY', '')
        self.api_url = api_url or os.environ.get('OPENAI_API_URL', 'https://api.openai.com/v1/chat/completions')

        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set it in the environment or pass it to the constructor.")

    def get_completion(self, prompt, model="gpt-4o", max_tokens=2000, temperature=0.7):
        """
        Get a completion from the OpenAI API

        Args:
            prompt (str): The prompt to send to the API
            model (str): The model to use (gpt-4o or gpt-4o-mini)
            max_tokens (int): Maximum number of tokens to generate
            temperature (float): Sampling temperature (0.0 to 1.0)

        Returns:
            str: The generated text
        """
        if model not in ["gpt-4o", "gpt-4o-mini"]:
            raise ValueError("Model must be 'gpt-4o' or 'gpt-4o-mini'")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for 4XX/5XX responses

            result = response.json()

            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception("No response generated")

        except requests.exceptions.RequestException as e:
            # Handle connection errors or API errors
            error_message = f"API request failed: {str(e)}"
            if response and hasattr(response, 'text'):
                try:
                    error_data = json.loads(response.text)
                    if 'error' in error_data and 'message' in error_data['error']:
                        error_message = f"API error: {error_data['error']['message']}"
                except:
                    error_message = f"API error: {response.text}"

            raise Exception(error_message)