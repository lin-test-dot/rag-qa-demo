from openai import OpenAI
from config import API_KEY, BASE_URL, CHAT_MODEL

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def answer(query, matched_chunks):
    context_text = "\n".join(matched_chunks)

    prompt = f"""
    你是一个严谨的助手。请严格根据以下【参考资料】回答问题。
    如果资料中没有，请回答“资料中未提及”。

    【参考资料】：
    {context_text}

    【问题】：
    {query}
    """

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content