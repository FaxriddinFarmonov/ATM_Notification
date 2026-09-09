import requests
import logging

logger = logging.getLogger(__name__)


class RegionOllamaService:
    BASE_URL = "http://localhost:11434/api/generate"
    MODEL = "qwen3:4b"
    session = requests.Session()

    @classmethod
    def generate(cls, prompt, timeout=60):
        try:
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
                timeout=timeout,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except Exception as e:
            logger.warning("RegionOllamaService error: %s", str(e))
            return f"Ollama AI tahlil xizmati vaqtincha javob bermadi: {str(e)}"

