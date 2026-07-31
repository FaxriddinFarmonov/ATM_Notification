import requests


class OllamaService:

    BASE_URL = "http://localhost:11434/api/generate"

    MODEL = "qwen3:4b"

    session = requests.Session()

    @classmethod
    def generate(cls, prompt):

        response = cls.session.post(

            cls.BASE_URL,

            json={
                "model": cls.MODEL,
                "prompt": prompt,
                "stream": False,
                "think": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "repeat_penalty": 1.2,
                    "num_predict": 2048,
                },
            },

            timeout=120,

        )
        response = requests.post(
            cls.BASE_URL,
            json={
                "model": cls.MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "repeat_penalty": 1.2,
                },
            },
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()


        return data["response"]


        return data.get("response", "")