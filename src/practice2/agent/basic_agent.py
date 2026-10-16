from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from utils.utils import load_file


@tool
def calculator(
    first_number: float,
    second_number: float,
    operation: str,
) -> float:
    """두 숫자의 사칙연산을 수행합니다."""

    if operation == "add":
        return first_number + second_number

    if operation == "subtract":
        return first_number - second_number

    if operation == "multiply":
        return first_number * second_number

    if operation == "divide":
        if second_number == 0:
            raise ValueError("0으로 나눌 수 없습니다.")

        return first_number / second_number

    raise ValueError(
        "지원하지 않는 연산입니다. "
        "add, subtract, multiply, divide 중 하나를 사용하세요."
    )


@tool
def get_company_name() -> str:
    """회사 이름을 반환합니다."""
    return "ABC Corporation"


def create_basic_agent():
    """Create and return the basic example Agent."""

    api_key = load_file(".env")

    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        api_key=api_key,
        temperature=0,
    )

    agent = create_agent(
        model=llm,
        tools=[calculator, get_company_name],
        system_prompt=(
            "You are a helpful assistant. "
            "Use the provided tools when they are useful. "
            "Answer the user in Korean."
        ),
    )

    return agent


if __name__ == "__main__":
    agent = create_basic_agent()

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": (
                    "우리 회사 이름과 125000원의 15%가 "
                    "얼마인지 알려주세요."
                ),
            }
        ]
    })

    print(result["messages"][-1].content)