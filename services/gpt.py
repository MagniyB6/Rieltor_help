import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def generate_post_text(prompt: str) -> str:
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты копирайтер, пиши как риелтор."},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content.strip()
