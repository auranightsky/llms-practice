from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from src.utils.utils import load_file
from src.agent.speaker_state import speaker_state
from src.agent.speaker_tools import create_speaker_tools


SYSTEM_PROMPT = """
You are a customer support and device management Agent for the
Samsung Music Studio WiFi speaker.

Rules:
1. Use search_manual to look up product instructions and troubleshooting.
2. Use get_speaker_status when the user asks about current settings.
3. Use change_speaker_setting when the user requests a setting change.
4. If a new Bluetooth pairing is requested while another device is
   connected, disconnect it first, then enter pairing mode.
5. Resetting the speaker is a destructive action. Try safer solutions first.
   Never reset unless the user has explicitly approved the reset.
   Set approved=True only after explicit approval from the user.
6. Use request_service if the issue remains unresolved.
7. Check tool results before responding.
8. Respond to the user in Korean.
9. This is a simulated speaker state. Do not claim to control real hardware.
10. Do not claim that a Bluetooth device has actually connected;
    pairing mode is only simulated.
""".strip()


def create_speaker_agent(retriever):
    """
    Create the speaker-support Agent.

    retriever:
        The retriever created from the parsed speaker manual.
    """

    api_key = load_file(".env")

    tools = create_speaker_tools(
        retriever=retriever,
        speaker_state=speaker_state,
    )

    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        api_key=api_key,
        temperature=0,
    )

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )

    return agent