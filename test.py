from langchain_openai import ChatOpenAI
from key import openai_key

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# 모델 초기화 (gpt-4 등 모델 지정 가능)
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    openai_api_key=openai_key # 여기서 키를 직접 넘겨줌
)

# 대화 메시지 구성
messages = [
    HumanMessage(content="안녕! 너 이름이 뭐야")
]

# 응답 생성
response = llm(messages)

# 결과 출력
print(response.content)