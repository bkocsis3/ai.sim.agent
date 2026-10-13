from langchain_openai import ChatOpenAI
from ai.config import settings

def get_gpt_5_4_mini():
    return ChatOpenAI(
        model="gpt-5.4-mini",
        temperature=0.2
    )