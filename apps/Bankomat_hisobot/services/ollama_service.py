import requests
import logging
import re

logger = logging.getLogger(__name__)


def clean_uzbek_text(text: str) -> str:
    if not text:
        return ""
    # Noo'rin yoki xato tarjimalarni rasmiy bank atamalariga aylantirish
    text = re.sub(r'(?:bilan\s+)?gaplash(?:a\s+)?olmaydi', "tarmoqqa ulanmagan", text, flags=re.IGNORECASE)
    text = re.sub(r'(?:bilan\s+)?gaplashmaydi', "operatsiyalar amalga oshirilmagan", text, flags=re.IGNORECASE)
    text = re.sub(r'gaplashish(?:ga)?\s+(?:imkoni|imkoniyati)\s+yo[\'\u2019`]?q', "tranzaksiya qayd etilmagan", text, flags=re.IGNORECASE)
    text = re.sub(r'gaplasha\s+olmasligini', "faoliyatsiz ekanligini", text, flags=re.IGNORECASE)
    
    # e'tiraf etiladi -> qayd etiladi
    text = re.sub(r"e[\'\u2019`]tiraf etiladi", "qayd etiladi", text, flags=re.IGNORECASE)
    text = re.sub(r"e[\'\u2019`]tiraf qilindi", "kuzatildi", text, flags=re.IGNORECASE)
    
    # o'zaro hisoblanayotgan -> tahlil qilinayotgan
    text = re.sub(r"o[\'\u2019`]zaro hisoblanayotgan", "tahlil qilinayotgan", text, flags=re.IGNORECASE)
    text = re.sub(r"келиши магни", "tashkil etdi", text, flags=re.IGNORECASE)
    text = re.sub(r"сомга", "so'mga", text, flags=re.IGNORECASE)
    text = re.sub(r"сому", "so'm", text, flags=re.IGNORECASE)
    text = re.sub(r"сом", "so'm", text, flags=re.IGNORECASE)

    return text.strip()


class OllamaService:
    BASE_URL = "http://localhost:11434/api/generate"
    MODEL = "qwen2.5:7b"
    FALLBACK_MODEL = "qwen3:4b"
    session = requests.Session()

    @classmethod
    def _call_model(cls, model_name: str, prompt: str, timeout: int = 120) -> str:
        try:
            payload = {
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "think": False,
                "options": {
                    "temperature": 0.2,
                    "top_p": 0.9,
                    "repeat_penalty": 1.15,
                    "num_predict": 2500,
                },
            }
            response = cls.session.post(cls.BASE_URL, json=payload, timeout=timeout)
            response.raise_for_status()
            data = response.json()

            text = data.get("response", "").strip()
            if not text and data.get("thinking"):
                text = data.get("thinking", "").strip()

            if "</think>" in text:
                parts = text.split("</think>")
                if parts[-1].strip():
                    text = parts[-1].strip()

            return clean_uzbek_text(text)
        except Exception as e:
            logger.warning("Ollama xatolik (%s): %s", model_name, str(e))
            return ""

    @classmethod
    def generate(cls, prompt: str, timeout: int = 120) -> str:
        res = cls._call_model(cls.MODEL, prompt, timeout=timeout)
        if res:
            return clean_uzbek_text(res)

        logger.info("%s javob bermadi, zaxira modelga o'tilmoqda...", cls.MODEL)
        res_fallback = cls._call_model(cls.FALLBACK_MODEL, prompt, timeout=timeout)
        if res_fallback:
            return clean_uzbek_text(res_fallback)

        return "Bankomat tahlilini yaratishda xatolik yuz berdi. Ollama xizmatini tekshiring."
