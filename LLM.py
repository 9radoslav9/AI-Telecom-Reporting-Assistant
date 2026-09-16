import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "inclusionai/ling-3.0-flash-vl:free"

SYSTEM_PROMPT = """Ти си асистент, който пише кратки бизнес резюмета на телеком данни.
Правила, които следваш стриктно:
1. Отговаряй ЕДИНСТВЕНО на български език, с коректна граматика.
2. Използвай САМО числата, подадени ти в данните. Никога не добавяй,
   не закръгляваш по различен начин и не измисляш стойности.
3. Пиши кратко — максимум 4-5 изречения, без излишни встъпления.
4. Не използвай markdown форматиране (без **, без списъци, без емотикони) — само чист текст.
5. За всеки елемент, който споменаваш конкретно (регион, месец, план),
   винаги цитирай точното число от данните, а не обобщение или диапазон
   (например пиши "Русе с 223.92 €.", не "региони между 165 и 176 €.").
6. Не пресмятай сам суми, средни стойности, брой елементи под определена
   граница или съотношения — споменавай само стойности, които са ти
   директно подадени в данните.
7. Валутата е винаги евро, изписвана със символа €. Никога не пиши "лв.",
   "лева" или "BGN" — задължително ползвай точно символа €, както е
   подаден в данните.
8. След фактическото резюме, добави ЕДНО кратко изречение с качествено
   бизнес наблюдение или препоръка (например за концентрация на приходи,
   регионални различия, или възможност за действие). Това изречение
   НЕ трябва да съдържа никакви числа — само описателна, качествена мисъл.
"""

def generate_summary(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
    data = response.json()

    return data["choices"][0]["message"]["content"]


SYSTEM_PROMPT_RAG = """Ти си асистент, който отговаря на въпроси за телеком бизнес данни,
използвайки САМО контекста, предоставен ти по-долу.

Правила:
1. Отговаряй единствено на база подадения контекст. Никога не добавяй
   информация, която не е изрично налична в него.
2. Ако контекстът не съдържа отговор на въпроса, кажи ясно: "Нямам
   достатъчно данни, за да отговоря на този въпрос." Не гадай и не измисляй.
3. Отговаряй на български, кратко (2-3 изречения), без markdown форматиране.
4. Валутата е винаги евро, изписвана със символа €.
5. Цитирай конкретните числа от контекста точно както са подадени.
"""


def generate_rag_answer(question: str, context_chunks: list[dict]) -> str:
    context_text = "\n".join(chunk["text"] for chunk in context_chunks)
    user_prompt = f"Контекст:\n{context_text}\n\nВъпрос: {question}"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT_RAG},
            {"role": "user", "content": user_prompt},
        ],
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
    data = response.json()

    return data["choices"][0]["message"]["content"]
