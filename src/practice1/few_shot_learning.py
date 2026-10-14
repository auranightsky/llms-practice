from openai import OpenAI
from utils import load_file

# Load API key
openai_api_key = load_file(".env")
print(openai_api_key is None)

client = OpenAI(api_key=openai_api_key)

# Few-shot examples
EXAMPLE_1_INPUT = """
회의 노트:
- 프로젝트 일정이 고객 요청으로 인해 지연되었습니다.
- 새로운 요구사항을 반영하기 위해 추가 작업이 필요합니다.
- 다음 주에 팀별로 진행 상황을 보고하기로 했습니다.
"""

EXAMPLE_1_OUTPUT = """
보고서:
**주요 논의 사항**: 프로젝트 일정이 고객의 새로운 요구사항으로 인해 지연되었습니다. 
이를 반영하기 위한 추가 작업이 필요합니다.

**결론**: 프로젝트 일정을 조정하기로 했습니다.

**후속 조치 계획**: 각 팀은 다음 주에 진행 상황을 보고할 예정입니다.
"""

EXAMPLE_2_INPUT = """
회의 노트:
- 새로운 마케팅 캠페인 시작에 대해 논의했습니다.
- 온라인 광고와 소셜 미디어를 통해 브랜드 인지도를 높일 계획입니다.
- 다음 주에 캠페인의 첫 번째 단계를 실행할 예정입니다.
"""

EXAMPLE_2_OUTPUT = """
보고서:
**주요 논의 사항**: 새로운 마케팅 캠페인을 시작하기로 결정했습니다. 
온라인 광고와 소셜 미디어를 통해 브랜드 인지도를 높일 계획입니다.

**결론**: 캠페인은 계획대로 진행될 것입니다.

**후속 조치 계획**: 캠페인의 첫 번째 단계가 다음 주에 시작될 예정입니다.
"""

def generate_report(meeting_notes):
    messages = [
        {
            "role": "system",
            "content": (
                "회의 노트를 보고 보고서를 작성하세요. "
                "보고서에는 주요 논의 사항, 결론, "
                "후속 조치 계획을 포함하세요."
            ),
        },

        # Few-shot example 1
        {
            "role": "user",
            "content": EXAMPLE_1_INPUT,
        },
        {
            "role": "assistant",
            "content": EXAMPLE_1_OUTPUT,
        },

        # Few-shot example 2
        {
            "role": "user",
            "content": EXAMPLE_2_INPUT,
        },
        {
            "role": "assistant",
            "content": EXAMPLE_2_OUTPUT,
        },

        # Actual meeting notes
        {
            "role": "user",
            "content": f"""회의 노트:{meeting_notes}""",
        },
    ]

    response = client.chat.completions.create(
        model="gpt-5.6-luna",
        messages=messages,
        max_completion_tokens=1500,
    )

    return response.choices[0].message.content


# Load actual meeting notes
meeting_notes = load_file("meeting_note.txt")

# Generate report
report = generate_report(meeting_notes)
print(report)
