
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from openai import OpenAI
from utils import load_file

# Load api key
openai_api_key = load_file(".env")
print(openai_api_key is None)

# Apply your api key
client = OpenAI(api_key=openai_api_key)

def generate(query):
    messages = [
        {"role": "system", "content": "다음은 마케팅 부서 회의의 미팅 노트입니다. 이 노트를 바탕으로 정돈된 보고서를 작성하세요. "},
        {"role": "system", "content": "보고서에는 회의의 주요 논의 사항, 결론, 후속 조치 계획이 포함되어야 합니다. "},
        {"role": "system", "content": f"미팅 노트는 다음과 같습니다: {query}"}
    ]
    response = client.chat.completions.create(
        model="gpt-5.6-luna",
        messages=messages,
        n=1,
        max_completion_tokens=1500)
    
    queries = response.choices[0].message.content.split('\n')
    queries = [q for q in queries if any(c.isalpha() for c in q)]
    return queries

# Open file data/meeting.txt
text   = load_file("meeting_note.txt", True)
query  = '\n'.join(text)
result = generate(query)
print("\n".join(result))
