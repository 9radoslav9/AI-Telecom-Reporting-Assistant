import os
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from LLM import MODEL


load_dotenv()

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

model = ChatOpenRouter(
    model=MODEL,
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{formatted_data}"),
])

chain = prompt | model | StrOutputParser()


def generate_summary(formatted_data: str) -> str:
    return chain.invoke({"formatted_data": formatted_data})



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

rag_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT_RAG),
    ("human", "Контекст:\n{context}\n\nВъпрос: {question}"),
])

rag_chain = rag_prompt | model | StrOutputParser()


def generate_rag_answer_langchain(question: str, context_chunks: list[dict]) -> str:
    context_text = "\n".join(chunk["text"] for chunk in context_chunks)
    return rag_chain.invoke({"context": context_text, "question": question})



CLASSIFY_SYSTEM_PROMPT = """Ти класифицираш въпроси за телеком бизнес данни в точно една от четири категории.

Категории:
- revenue: въпроси за приходи, пари, евро/€, кой регион печели повече или по-малко
- customers: въпроси за брой нови клиенти, регистрации, конкретни месеци на регистрация
- usage: въпроси за GB данни, минути разговори, SMS, или плановете Basic/Standard/Premium
- general: всичко останало — твърде общи, двусмислени, извън тези три теми,
  или изискващи сравнение/изчисление, което не е директно налично

Отговори ЕДИНСТВЕНО с една от четирите думи: revenue, customers, usage, general.
Без обяснение, без пунктуация, без нищо друго.
Ако не си сигурен на 100%, отговори с general — по-безопасно е да отидеш към
отворения RAG отговор, отколкото погрешно да насочиш към агрегация, която не
пасва на реалния въпрос.
"""

classify_prompt = ChatPromptTemplate.from_messages([
    ("system", CLASSIFY_SYSTEM_PROMPT),
    ("human", "{question}"),
])

classify_chain = classify_prompt | model | StrOutputParser()

VALID_ROUTES = {"revenue", "customers", "usage", "general"}


def classify_question(question: str) -> str:
    raw_result = classify_chain.invoke({"question": question}).strip().lower()

    for route in VALID_ROUTES:
        if route in raw_result:
            return route

    return "general"